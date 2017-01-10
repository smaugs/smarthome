import logging
from .item import Item

class ItemBuilder():
    __items = []  # all item paths as string ['env.core.version','env.core.start','env.core.memory',.... ]
    __children = []  # all top items as object [Item:env, Item: env_init, Item:env_daily, ....]
    __item_dict = {}  # dictionary with all item paths and objects  {'env.system.name':Item:env.system.name, 'test.item1':Item: test.item1, .....}

    def __init__(self,sh):
        self.logger = logging.getLogger(__name__)
        self._sh = sh
        self.scheduler= sh.scheduler
#    #FIXME: Remove after test
#    def now(self):
#        return self._sh.now()
#
#    # FIXME: Remove after test
#    def return_plugins(self):
#        return self._sh.return_plugins()


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
                    #FIXME: remove
                    if child_path == 'env.system.libs':
                        b=True

                    child = Item(self, parent, child_path, value) #Itembuilder , parent, path, value
                    child.fill_attribs(value)
                    child.read_cache()
                    parent.append_child(child,attr)
                    self.build_itemtree(value,child)
                  #  if not isinstance(parent, self._sh.__class__):
                   #     for item in parent.return_children():
                    #        vars(parent)[item._name] = item

                except Exception as e:
                    self.logger.error("Item {}: problem creating: ()".format(child_path, e))
                    raise  e
                else:
                    # vars(self._sh)[attr] = child  # move down
                    self.add_item(parent, child_path, child)
                    #sh.append_child(child) ->
                    #parent.append_child(child)
            #else:
        #if not isinstance(parent, self._sh.__class__):
        #    parent.fill_attribs( item_conf)
        #    parent.read_cache()
           # parent._set_type(parent._type)

    def get_items(self):
        return self.__children, self.__item_dict, self.__items
