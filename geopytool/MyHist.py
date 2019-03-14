from geopytool.ImportDependence import *
from geopytool.CustomClass import *
#from geopytool.TableViewer import TableViewer


class MyHist(AppForm):
    _df = pd.DataFrame()
    _changed = False

    xlabel = r'Item Slected'
    ylabel = r'Frequency'

    reference = 'Yu, Q.-Y., Bagas, L., Yang, P.-H., Zhang, D., GeoPyTool: a cross-platform software solution for common geological calculations and plots, Geoscience Frontiers (2018), doi: 10.1016/j.gsf.2018.08.001..'

    whole_labels = []
    all_labels = []
    all_colors = []
    all_markers = []
    all_alpha = []
    all_data_list = []


    def __init__(self, parent=None, df=pd.DataFrame(),filename= '/'):
        QWidget.__init__(self, parent)

        self.setWindowTitle('Hist')
        self.FileName_Hint = ''
        self._df = df
        self.filename= filename

        if (len(df) > 0):
            self._changed = True
            # print('DataFrame recieved to AppForm')

        self.create_main_frame()
        self.create_status_bar()



    def create_main_frame(self):
        self.resize(1000, 800)
        self.main_frame = QWidget()
        self.dpi = 128
        self.fig = Figure((18.0, 12.0), dpi=self.dpi)
        self.fig.subplots_adjust(hspace=0.5, wspace=0.5, left=0.1, bottom=0.2, right=0.7, top=0.9)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.main_frame)
        self.axes = self.fig.add_subplot(111)
        self.axes.axis('off')
        # Create the navigation toolbar, tied to the canvas
        self.mpl_toolbar = NavigationToolbar(self.canvas, self.main_frame)

        # Other GUI controls


        self.save_button = QPushButton('&Save Img')
        self.save_button.clicked.connect(self.saveImgFile)

        self.legend_cb = QCheckBox('&Legend')
        self.legend_cb.setChecked(True)
        self.legend_cb.stateChanged.connect(self.MyHist)  # int


        self.density_cb = QCheckBox('&Density')
        self.density_cb.setChecked(True)
        self.density_cb.stateChanged.connect(self.MyHist)  # int

        self.stack_cb = QCheckBox('&Stack')
        self.stack_cb.setChecked(True)
        self.stack_cb.stateChanged.connect(self.MyHist)  # int


        self.combine_cb = QCheckBox('&Combine')
        self.combine_cb.setChecked(False)
        self.combine_cb.stateChanged.connect(self.MyHist)  # int


        self.overlap_cb = QCheckBox('&Overlap')
        self.overlap_cb.setChecked(False)
        self.overlap_cb.stateChanged.connect(self.MyHist)  # int

        self.clean_df = self.Slim(self._df)

        print(self.clean_df )

        self.x_element = QSlider(Qt.Horizontal)
        self.x_element.setRange(0, len(self.clean_df.columns.values.tolist() ) - 1)
        self.x_element.setValue(0)
        self.x_element.setTracking(True)
        self.x_element.setTickPosition(QSlider.TicksBothSides)
        self.x_element.valueChanged.connect(self.MyHist)  # int
        self.x_element_label = QLabel('component')


        self.hbox = QHBoxLayout()

        for w in [self.save_button,self.legend_cb,self.density_cb,self.stack_cb,self.overlap_cb,self.combine_cb,self.x_element_label,self.x_element]:
            self.hbox.addWidget(w)
            self.hbox.setAlignment(w, Qt.AlignVCenter)

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.mpl_toolbar)
        self.vbox.addWidget(self.canvas)
        self.vbox.addLayout(self.hbox)
        self.textbox = GrowingTextEdit(self)
        self.textbox.setText(self.reference)

        self.vbox.addWidget(self.textbox)

        self.main_frame.setLayout(self.vbox)
        self.setCentralWidget(self.main_frame)


    def Slim(self,df= pd.DataFrame()):

        ItemsAvalibale = df.columns.values.tolist()
        if 'Label' in ItemsAvalibale:
            df = df.set_index('Label')

        df = df.dropna(axis=1,how='all')

        ItemsToTest = ['Number', 'Tag', 'Name', 'Author', 'DataType', 'Marker', 'Color', 'Size', 'Alpha',
                       'Style', 'Width']

        for i in ItemsToTest:
            if i in ItemsAvalibale:
                df = df.drop(i, 1)

        df = df.apply(pd.to_numeric, errors='coerce')

        return(df)

    def MyHist(self):

        fontprop = font_manager.FontProperties(family='sans-serif',
                                               size=9,
                                               fname=ttfFontProp.fname,
                                               stretch=ttfFontProp.stretch,
                                               style=ttfFontProp.style,
                                               variant=ttfFontProp.variant,
                                               weight=ttfFontProp.weight)


        self.setWindowTitle('Hist')
        self.textbox.setText(self.reference)
        self.axes.clear()
        #self.axes.axis('off')
        self.axes.set_xlabel(self.xlabel,fontproperties =fontprop)
        self.axes.set_ylabel(self.ylabel,fontproperties =fontprop)
        ##self.axes.spines['top'].set_color('none')

        a = int(self.x_element.value())
        items=self.clean_df.columns.values.tolist()
        self.axes.set_xlabel(items[a])
        self.x_element_label.setText(items[a])

        self.all_labels=[]
        self.all_colors=[]
        self.all_markers=[]
        self.all_alpha=[]
        self.all_data_list=[]


        if (self.combine_cb.isChecked()):

            self.all_data_list = self._df[items[a]]


            if (self.density_cb.isChecked()):
                self.axes.hist(self.all_data_list,density=True, facecolor= 'grey', alpha= 0.6,
                           label=self.getFileName([self.filename]), edgecolor='k')
            else:
                self.axes.hist(self.all_data_list, density=False, facecolor= 'grey', alpha= 0.6,
                           label=self.getFileName([self.filename]), edgecolor='k')


        else:

            for i in range(len(self._df)):
                target = self._df.at[i, 'Label']
                color = self._df.at[i, 'Color']
                marker = self._df.at[i, 'Marker']
                alpha = self._df.at[i, 'Alpha']

                if target not in self.all_labels:
                    self.all_labels.append(target)
                    self.all_colors.append(color)
                    self.all_markers.append(marker)
                    self.all_alpha.append(alpha)

            self.whole_labels = self.all_labels

            for j in self.all_labels:
                tmp_data_list = []
                for i in range(len(self._df)):
                    target = self._df.at[i, 'Label']
                    if target == j:
                        tmp_data_list.append(self._df.at[i,items[a]])

                self.all_data_list.append(tmp_data_list)

            if (self.stack_cb.isChecked()):
                pass

                if (self.density_cb.isChecked()):

                    self.axes.set_ylabel(self.ylabel+' Density')

                    N, bins, patches = self.axes.hist(self.all_data_list, density=True, stacked=True,edgecolor='k',alpha= 0.6)
                else:
                    N, bins, patches = self.axes.hist(self.all_data_list, density=False, stacked=True,edgecolor='k',alpha= 0.6)


                    #patches[i].set_facecolor('red')
                width = (bins[1] - bins[0]) * 0.4

                tmp_label_check=[]
                for k in range(len(patches)):
                    for p in patches[k]:
                        p.set_facecolor(self.all_colors[k])
                        p.set_alpha(self.all_alpha[k])

                        if self.all_labels[k] not in tmp_label_check:
                            tmp_label_check.append(self.all_labels[k])
                            p.set_label(self.all_labels[k])


            else:

                if (self.overlap_cb.isChecked()):
                    for k in range(len(self.all_labels)):

                        if (self.density_cb.isChecked()):

                            self.axes.set_ylabel(self.ylabel+' Density')

                            self.axes.hist(self.all_data_list[k], density=True, facecolor= self.all_colors[k], alpha= self.all_alpha[k],label=self.all_labels[k],edgecolor ='k')
                        else:
                            self.axes.hist(self.all_data_list[k], density=False, facecolor= self.all_colors[k], alpha= self.all_alpha[k],label=self.all_labels[k],edgecolor ='k')

                else:
                    if (self.density_cb.isChecked()):

                        self.axes.set_ylabel(self.ylabel+' Density')

                        N, bins, patches = self.axes.hist(self.all_data_list, density=True, stacked=False,edgecolor='k',alpha= 0.6)
                    else:
                        N, bins, patches = self.axes.hist(self.all_data_list, density=False, stacked=False,edgecolor='k',alpha= 0.6)


                        #patches[i].set_facecolor('red')

                    tmp_label_check=[]
                    for k in range(len(patches)):
                        for p in patches[k]:
                            p.set_facecolor(self.all_colors[k])
                            p.set_alpha(self.all_alpha[k])

                            if self.all_labels[k] not in tmp_label_check:
                                tmp_label_check.append(self.all_labels[k])
                                p.set_label(self.all_labels[k])



        if (self.legend_cb.isChecked()):
            self.axes.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0, prop=fontprop)

        self.canvas.draw()



    def Explain(self):

        #self.OutPutData = self.OutPutData.set_index('Label')

        self.tablepop = TableViewer(df=self.OutPutData,title='Hist Result')
        self.tablepop.show()