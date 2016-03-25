class myColumndataSource(ColumnDataSource):
    def __init__(self,*args, **kw):
        self._data={}
        self._selected={
        '0d': {'glyph': None, 'indices': []},
        '1d': {'indices': []},
        '2d': {'indices': []}
        }
        ColumnDataSource.__init__(self,*args, **kw)
        self.tags=[]
    @property
    def data(self):
        return self._data
    @data.setter
    def data(self,new_data):
        new_names={}
        for i,name in enumerate(new_data["Pulsar"]):
            new_names[name]=i
        new_indices=[]
        for n in self.tags.keys():
            if n in new_names.keys():
                i=new_names[n]
                self.tags[n]=i
                new_indices.append(i)
            else:
                del self.tags[n]
        self.selected["1d"]["indices"]=new_indices
        #for name in self.current_names and not in new_names:
        self._data=new_data

    @property
    def selected(self):
        return self._selected

    @selected.setter
    def selected(self,new_selected):
        selected_indices=new_selected["1d"]["indices"]
        data_names={}
        for i,name in enumerate(self.data["Pulsar"]):
            data_names[name]=i

        for i,name in enumerate(self.data["Pulsar"]):
            data_names[i]=name
        self.tags={} #clear
        for j,name in data_names.iteritems():
            if j in selected_indices:
                self.tags[name]=j

    @property
    def tags(self):
        import inspect
        curframe = inspect.currentframe()
        calframe = inspect.getouterframes(curframe, 2)
        caller_name=calframe[1][3]
        if "update" or "filtered" or "onclick" in caller_name:
            return {}
        else:

    # def update_selction(self):
    #     for i,name in enumerate(self.data["Pulsar"]):
    #         self.current_names[name]=i
    #
    #     for name in self.global_names:
    #         self.current_selection.append(self.current_names[name])
    #     self.selected["1d"]["indices"]=self.current_selection
