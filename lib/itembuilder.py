import logging
from .item import Item

class ItemBuilder():
    __items = []  # all item paths as string ['env.core.version','env.core.start','env.core.memory',.... ]
    #__children = []  # all top items as object [Item:env, Item: env_init, Item:env_daily, ....]
    __item_dict = {}  # dictionary with all item paths and objects  {'env.system.name':Item:env.system.name, 'test.item1':Item: test.item1, .....}

    def __init__(self,sh):
        self.logger = logging.getLogger(__name__)
        self._sh = sh
        self.scheduler= sh.scheduler

    def run_items(self):
        # run prerun and init methods.
        for item in self.return_items():
            item._init_prerun()
        for item in self.return_items():
            item._init_run()

    def return_items(self):
        for item in self.__items:
            yield self.__item_dict[item]

    def add_item(self, parent, path, item):
        """
        add item methode, wird auch von Item aufgerufen!
        :param path:
        :param item:
        :return:
        """

        if path not in self.__items:
            self.__items.append(path)
        self.__item_dict[path] = item

    def build_itemtree(self, item_conf, parent):

        for attr, value in item_conf.items():
            if isinstance(value, dict):
                if isinstance(parent,self._sh.__class__):
                    child_path = attr
                elif isinstance(parent,Item):
                    child_path = parent._path+ '.'+ attr
                try:

                    child = Item(self._sh, parent, child_path, value) #Itembuilder , parent, path, value
                    child.fill_attribs(value)
                    child.read_cache()
                    parent.append_child(child,attr)
                    self.build_itemtree(value,child)

                except Exception as e:
                    self.logger.error("Item {}: problem creating: ()".format(child_path, e))
                    raise  e
                else:
                    self.add_item(parent, child_path, child)


    def get_items(self):
        return self.__item_dict, self.__items
