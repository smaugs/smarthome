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
    #FIXME: Remove after test
    def now(self):
        return self._sh.now()

    # FIXME: Remove after test
    def return_plugins(self):
        return self._sh.return_plugins()




    def add_item(self, path, item):
        """
        add item methode, wird auch von Item aufgerufen!
        :param path:
        :param item:
        :return:
        """

        if path not in self.__items:
            self.__items.append(path)
        self.__item_dict[path] = item

    def build_itemtree(self, item_conf):
        for attr, value in item_conf.items():
            if isinstance(value, dict):
                child_path = attr
                try:
                    child = Item(self, self._sh, child_path, value)
                except Exception as e:
                    self.logger.error("Item {}: problem creating: ()".format(child_path, e))
                    raise  e
                else:
                    # vars(self._sh)[attr] = child  # move down
                    self.add_item(child_path, child)
                    #sh.append_child(child) ->
                    self.__children.append(child)


        return self.__children, self.__item_dict, self.__items
