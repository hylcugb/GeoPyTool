from geopytool.ImportDependence import *
from geopytool.CustomClass import *

class Harker(AppForm):
    Lines = []
    Tags = []

    BaseData =pd.DataFrame()

    description = 'Harker diagram'
    usefulelements = ['SiO2',
                      'TiO2',
                      'Al2O3',
                      'TFe2O3',
                      'Fe2O3',
                      'FeO',
                      'TFe',
                      'MnO',
                      'MgO',
                      'CaO',
                      'Na2O',
                      'K2O',
                      'P2O5',
                      'Loi',
                      'DI',
                      'Mg#',
                      'Li',
                      'Be',
                      'Sc',
                      'V',
                      'Cr',
                      'Co',
                      'Ni',
                      'Cu',
                      'Zn',
                      'Ga',
                      'Ge',
                      'Rb',
                      'Sr',
                      'Y',
                      'Zr',
                      'Nb',
                      'Cs',
                      'Ba',
                      'La',
                      'Ce',
                      'Pr',
                      'Nd',
                      'Sm',
                      'Eu',
                      'Gd',
                      'Tb',
                      'Dy',
                      'Ho',
                      'Er',
                      'Tm',
                      'Yb',
                      'Lu',
                      'III',
                      'Ta',
                      'Pb',
                      'Th',
                      'U']
    unuseful = ['Name',
                'Author',
                'DataType',
                'Label',
                'Marker',
                'Color',
                'Size',
                'Alpha',
                'Style',
                'Width',
                'Tag']

    itemstocheck = ['Al2O3', 'MgO', 'FeO', 'Fe2O3','CaO', 'Na2O', 'K2O', 'TiO2', 'P2O5', 'SiO2']

    def __init__(self, parent=None, df=pd.DataFrame()):
        QMainWindow.__init__(self, parent)
        self.setWindowTitle('Harker diagram')

        self.FileName_Hint='Harker'

        self.items = []

        self._df = df
        if (len(df) > 0):
            self._changed = True
            # print('DataFrame recieved to Harker')

        self.raw = df
        self.rawitems = self.raw.columns.values.tolist()

        for i in self.rawitems:
            if i not in self.unuseful:
                self.items.append(i)
            else:
                pass

        self.create_main_frame()
        self.create_status_bar()


    def Check(self,df=pd.DataFrame()):

        row = df.index.tolist()
        col = df.columns.tolist()
        itemstocheck = self.itemstocheck
        checklist = list((set(itemstocheck).union(set(col))) ^ (set(itemstocheck) ^ set(col)))
        if len(checklist) >= (len(itemstocheck)-1) and ('FeO' in checklist or 'Fe2O3' in checklist):
            self.OutPutCheck = True
        else:
            self.OutPutCheck = False
        return(self.OutPutCheck)

    def create_main_frame(self):
        self.resize(800, 1000)
        self.main_frame = QWidget()
        self.dpi = 128
        self.fig ,self.axes= plt.subplots(4, 2,figsize=(15, 20),dpi=self.dpi)
        self.fig.subplots_adjust(hspace=0.2, wspace=0.4,left=0.1, bottom=0.2, right=0.7, top=0.95)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.main_frame)

        # Create the navigation toolbar, tied to the canvas
        self.mpl_toolbar = NavigationToolbar(self.canvas, self.main_frame)

        # Other GUI controls

        
        self.save_img_button = QPushButton('&Save IMG')
        self.save_img_button.clicked.connect(self.saveImgFile)

        self.save_predict_button = QPushButton('&Show Predict Result')
        self.save_predict_button.clicked.connect(self.showPredictResult)

        self.load_data_button = QPushButton('&Add Data to Test')
        self.load_data_button.clicked.connect(self.loadDataToTest)


        self.seter_left_label = QLabel('Left')
        self.seter_left = QLineEdit(self)
        self.seter_left.textChanged[str].connect(self.Harker)
        self.seter_right_label = QLabel('Right')
        self.seter_right = QLineEdit(self)
        self.seter_right.textChanged[str].connect(self.Harker)


        #self.result_button = QPushButton('&Result')
        #self.result_button.clicked.connect(self.Harker)


        self.legend_cb = QCheckBox('&Legend')
        self.legend_cb.setChecked(True)
        self.legend_cb.stateChanged.connect(self.Harker)  # int


        self.show_load_data_cb = QCheckBox('&Show Loaded Data')
        self.show_load_data_cb.setChecked(True)
        self.show_load_data_cb.stateChanged.connect(self.Harker)  # int

        self.show_data_index_cb = QCheckBox('&Show Data Index')
        self.show_data_index_cb.setChecked(False)
        self.show_data_index_cb.stateChanged.connect(self.Harker)  # int


        self.shape_cb= QCheckBox('&Shape')
        self.shape_cb.setChecked(False)
        self.shape_cb.stateChanged.connect(self.Harker)  # int


        self.hyperplane_cb= QCheckBox('&Hyperplane')
        self.hyperplane_cb.setChecked(False)
        self.hyperplane_cb.stateChanged.connect(self.Harker)  # int


        #
        # Layout with box sizers
        #
        self.hbox = QHBoxLayout()

        for w in [self.seter_left_label ,self.seter_left,self.seter_right_label ,self.seter_right, self.legend_cb, self.show_load_data_cb, self.show_data_index_cb, self.shape_cb, self.hyperplane_cb,self.save_img_button,self.load_data_button,self.save_predict_button]:
            self.hbox.addWidget(w)
            self.hbox.setAlignment(w, Qt.AlignVCenter)

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.mpl_toolbar)
        self.vbox.addWidget(self.canvas)
        self.vbox.addLayout(self.hbox)


        self.textbox = GrowingTextEdit(self)
        self.textbox.setText(self.reference+self.description)

        self.vbox.addWidget(self.textbox)

        self.main_frame.setLayout(self.vbox)
        self.setCentralWidget(self.main_frame)
        w=self.width()
        h=self.height()

        self.seter_left_label.setFixedWidth(w / 20)
        self.seter_left.setFixedWidth(w / 20)
        self.seter_right_label.setFixedWidth(w / 20)
        self.seter_right.setFixedWidth(w / 20)

    def Harker(self):

        self.WholeData = []

        #raw = self._df


        raw = self.CleanDataFile(self._df)

        if self.Check(df=raw):
            pass


        itemstoshow = [r'$Al_2O_3$', r'$MgO$', r'$Fe2O3_{Total}$', r'$CaO$', r'$Na_2O$', r'$K_2O$', r'$TiO_2$', r'$P_2O_5$', r'$SiO_2$', ]

        self.axes[0, 0].clear()
        #self.axes[0, 0].set_xlim(45, 75)
        self.axes[0, 0].set_ylabel(itemstoshow[0])
        self.axes[0,0].set_xticks([45,50,55,60,65,70,75])
        self.axes[0, 0].set_xticklabels('')

        self.axes[0, 1].clear()
        #self.axes[0, 1].set_xlim(45, 75)
        self.axes[0, 1].set_ylabel(itemstoshow[1])
        self.axes[0,1].set_xticks([45,50,55,60,65,70,75])
        self.axes[0, 1].set_xticklabels('')

        self.axes[1,0].clear()
        #self.axes[1,0].set_xlim(45, 75)
        self.axes[1,0].set_ylabel(itemstoshow[2])
        self.axes[1,0].set_xticks([45,50,55,60,65,70,75])
        self.axes[1, 0].set_xticklabels('')


        self.axes[1,1].clear()
        #self.axes[1,1].set_xlim(45, 75)
        self.axes[1,1].set_ylabel(itemstoshow[3])
        self.axes[1,1].set_xticks([45,50,55,60,65,70,75])
        self.axes[1, 1].set_xticklabels('')

        self.axes[2,0].clear()
        #self.axes[2,0].set_xlim(45, 75)
        self.axes[2,0].set_ylabel(itemstoshow[4])
        self.axes[2,0].set_xticks([45,50,55,60,65,70,75])
        self.axes[2, 0].set_xticklabels('')

        self.axes[2,1].clear()
        #self.axes[2,1].set_xlim(45, 75)
        self.axes[2,1].set_ylabel(itemstoshow[5])
        self.axes[2,1].set_xticks([45,50,55,60,65,70,75])
        self.axes[2, 1].set_xticklabels('')

        self.axes[3,0].clear()
        #self.axes[3,0].set_xlim(45, 75)
        self.axes[3,0].set_ylabel(itemstoshow[6])
        self.axes[3, 0].set_xticks([45,50,55,60,65,70,75])

        self.axes[3, 0].set_xticklabels([45,50,55,60,65,70,75])

        self.axes[3,0].set_xlabel(itemstoshow[8])



        self.axes[3,1].clear()
        #self.axes[3,1].set_xlim(45, 75)
        self.axes[3,1].set_ylabel(itemstoshow[7])
        self.axes[3, 1].set_xticks([45,50,55,60,65,70,75])
        self.axes[3, 1].set_xticklabels([45,50,55,60,65,70,75])
        self.axes[3,1].set_xlabel(itemstoshow[8])
        try:
            left = float(self.seter_left.text())
            # if( type(left) == int or type(left)== float or type(left)== np.float ):pass
            self.axes[0, 1].set_xlim(left=left)
            self.axes[0, 0].set_xlim(left=left)
            self.axes[1, 0].set_xlim(left=left)
            self.axes[1, 1].set_xlim(left=left)
            self.axes[2, 0].set_xlim(left=left)
            self.axes[2, 1].set_xlim(left=left)
            self.axes[3, 0].set_xlim(left=left)
            self.axes[3, 1].set_xlim(left=left)
            pass
        except Exception as e:
            pass
            #self.ErrorEvent(text=repr(e))
        try:
            right = float(self.seter_right.text())
            self.axes[0, 1].set_xlim(right=right)
            self.axes[0, 0].set_xlim(right=right)
            self.axes[1, 0].set_xlim(right=right)
            self.axes[1, 1].set_xlim(right=right)
            self.axes[2, 0].set_xlim(right=right)
            self.axes[2, 1].set_xlim(right=right)
            self.axes[3, 0].set_xlim(right=right)
            self.axes[3, 1].set_xlim(right=right)
            pass
        except Exception as e:
            pass
            #self.ErrorEvent(text=repr(e))

        Al2O3_plot = self.axes[0, 0]
        MgO_plot = self.axes[0, 1]
        FeTotal_plot = self.axes[1, 0]
        CaO_plot = self.axes[1, 1]
        Na2O_plot = self.axes[2, 0]
        K2O_plot = self.axes[2, 1]
        TiO2_plot = self.axes[3, 0]
        P2O5_plot = self.axes[3, 1]

        PointLabels = []
        PointColors = []

        for i in range(len(raw)):
            if (raw.at[i, 'Label'] in PointLabels or raw.at[i, 'Label'] == ''):
                TmpLabel = ''
            else:
                PointLabels.append(raw.at[i, 'Label'])
                TmpLabel = raw.at[i, 'Label']
            if (raw.at[i, 'Color'] in PointColors or raw.at[i, 'Color'] == ''):
                pass
            else:
                PointColors.append(raw.at[i, 'Color'])


            Al2O3, MgO, FeO, Fe2O3, CaO, Na2O, K2O, TiO2, P2O5, SiO2 = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0

            Al2O3 = raw.at[i,'Al2O3']
            MgO = raw.at[i, 'MgO']
            CaO = raw.at[i,'CaO']
            Na2O = raw.at[i, 'Na2O']
            K2O = raw.at[i, 'K2O']
            TiO2 = raw.at[i, 'TiO2']
            P2O5 = raw.at[i, 'P2O5']
            SiO2 = raw.at[i, 'SiO2']
            if ('FeO' in raw.columns.tolist()):
                FeO=raw.at[i, 'FeO']
            if ('Fe2O3' in raw.columns.tolist()):
                Fe2O3=raw.at[i, 'Fe2O3']
            FeTotal= FeO/72*80+Fe2O3
            if ('TFeO' in raw.columns.tolist()):
                FeTotal=raw.at[i, 'TFeO']
            if ('TFe2O3' in raw.columns.tolist()):
                FeTotal=raw.at[i, 'TFe2O3']

            Al2O3_plot.scatter(SiO2, Al2O3, marker=raw.at[i, 'Marker'], s=raw.at[i, 'Size'], color=raw.at[i, 'Color'],
                               alpha=raw.at[i, 'Alpha'], label=TmpLabel)
            MgO_plot.scatter(SiO2, MgO, marker=raw.at[i, 'Marker'], s=raw.at[i, 'Size'], color=raw.at[i, 'Color'],
                             alpha=raw.at[i, 'Alpha'], label=TmpLabel)
            FeTotal_plot.scatter(SiO2, FeTotal, marker=raw.at[i, 'Marker'], s=raw.at[i, 'Size'],
                                 color=raw.at[i, 'Color'], alpha=raw.at[i, 'Alpha'], label=TmpLabel)
            CaO_plot.scatter(SiO2, CaO, marker=raw.at[i, 'Marker'], s=raw.at[i, 'Size'], color=raw.at[i, 'Color'],
                             alpha=raw.at[i, 'Alpha'], label=TmpLabel)
            Na2O_plot.scatter(SiO2, Na2O, marker=raw.at[i, 'Marker'], s=raw.at[i, 'Size'], color=raw.at[i, 'Color'],
                             alpha=raw.at[i, 'Alpha'], label=TmpLabel)
            K2O_plot.scatter(SiO2, K2O, marker=raw.at[i, 'Marker'], s=raw.at[i, 'Size'], color=raw.at[i, 'Color'],
                              alpha=raw.at[i, 'Alpha'], label=TmpLabel)
            TiO2_plot.scatter(SiO2, TiO2, marker=raw.at[i, 'Marker'], s=raw.at[i, 'Size'], color=raw.at[i, 'Color'],
                              alpha=raw.at[i, 'Alpha'], label=TmpLabel)
            P2O5_plot.scatter(SiO2, P2O5, marker=raw.at[i, 'Marker'], s=raw.at[i, 'Size'], color=raw.at[i, 'Color'],
                              alpha=raw.at[i, 'Alpha'], label=TmpLabel)


        Al2O3_dic = {}
        MgO_dic = {}
        CaO_dic = {}
        Na2O_dic = {}
        K2O_dic = {}
        TiO2_dic = {}
        P2O5_dic = {}
        SiO2_dic = {}
        FeTotal_dic = {}
        FeTotal_list=[]


        print(self.BaseData)

        for i in PointLabels:

            Al2O3_dic[i] = []
            MgO_dic[i] = []
            CaO_dic[i] = []
            Na2O_dic[i] = []
            K2O_dic[i] = []
            TiO2_dic[i] = []
            P2O5_dic[i] = []
            SiO2_dic[i] = []
            FeTotal_dic[i] = []


        for i in range(len(raw)):
            Alpha = raw.at[i, 'Alpha']
            Marker = raw.at[i, 'Marker']
            Label = raw.at[i, 'Label']

            Al2O3_test = raw.at[i, 'Al2O3']
            MgO_test = raw.at[i, 'MgO']
            CaO_test = raw.at[i, 'CaO']
            Na2O_test = raw.at[i, 'Na2O']
            K2O_test = raw.at[i, 'K2O']
            TiO2_test = raw.at[i, 'TiO2']
            P2O5_test = raw.at[i, 'P2O5']
            SiO2_test = raw.at[i, 'SiO2']



            if ('FeO' in raw.columns.tolist()):
                FeO=raw.at[i, 'FeO']

            if ('Fe2O3' in raw.columns.tolist()):
                Fe2O3=raw.at[i, 'Fe2O3']

            FeTotal= FeO/72*80+Fe2O3

            if ('TFeO' in raw.columns.tolist()):
                FeTotal=raw.at[i, 'TFeO']

            if ('TFe2O3' in raw.columns.tolist()):
                FeTotal=raw.at[i, 'TFe2O3']


            FeTotal_test = FeTotal

            Al2O3_dic[Label].append(Al2O3_test)
            MgO_dic[Label].append(MgO_test)
            CaO_dic[Label].append(CaO_test)
            Na2O_dic[Label].append(Na2O_test)
            K2O_dic[Label].append(K2O_test)
            TiO2_dic[Label].append(TiO2_test)
            P2O5_dic[Label].append(P2O5_test)
            SiO2_dic[Label].append(SiO2_test)
            FeTotal_dic[Label].append(FeTotal_test)
            FeTotal_list.append(FeTotal_test)

        if (self.shape_cb.isChecked()):
            for i in PointLabels:

                DensityColorMap = 'Greys'
                DensityAlpha = 0.1
                DensityLineColor = PointColors[PointLabels.index(i)]
                DensityLineAlpha = 0.3


                Al2O3_Contourf_Result=self.DrawContourf(xlist= SiO2_dic[i],ylist=Al2O3_dic[i])
                if Al2O3_Contourf_Result[0]==True:
                    Al2O3_plot.contourf(Al2O3_Contourf_Result[1], Al2O3_Contourf_Result[2], Al2O3_Contourf_Result[3], cmap=DensityColorMap, alpha=DensityAlpha)
                    Al2O3_plot.contour(Al2O3_Contourf_Result[1], Al2O3_Contourf_Result[2], Al2O3_Contourf_Result[3], colors=DensityLineColor, alpha=DensityLineAlpha)

                MgO_Contourf_Result=self.DrawContourf(xlist= SiO2_dic[i],ylist=MgO_dic[i])
                if MgO_Contourf_Result[0]==True:
                    MgO_plot.contourf(MgO_Contourf_Result[1], MgO_Contourf_Result[2], MgO_Contourf_Result[3], cmap=DensityColorMap, alpha=DensityAlpha)
                    MgO_plot.contour(MgO_Contourf_Result[1], MgO_Contourf_Result[2], MgO_Contourf_Result[3], colors=DensityLineColor, alpha=DensityLineAlpha)

                FeTotal_Contourf_Result=self.DrawContourf(xlist= SiO2_dic[i],ylist=FeTotal_dic[i])
                if FeTotal_Contourf_Result[0]==True:
                    FeTotal_plot.contourf(FeTotal_Contourf_Result[1], FeTotal_Contourf_Result[2], FeTotal_Contourf_Result[3], cmap=DensityColorMap, alpha=DensityAlpha)
                    FeTotal_plot.contour(FeTotal_Contourf_Result[1], FeTotal_Contourf_Result[2], FeTotal_Contourf_Result[3], colors=DensityLineColor, alpha=DensityLineAlpha)

                CaO_Contourf_Result=self.DrawContourf(xlist= SiO2_dic[i],ylist=CaO_dic[i])
                if CaO_Contourf_Result[0]==True:
                    CaO_plot.contourf(CaO_Contourf_Result[1], CaO_Contourf_Result[2], CaO_Contourf_Result[3], cmap=DensityColorMap, alpha=DensityAlpha)
                    CaO_plot.contour(CaO_Contourf_Result[1], CaO_Contourf_Result[2], CaO_Contourf_Result[3], colors=DensityLineColor, alpha=DensityLineAlpha)

                Na2O_Contourf_Result=self.DrawContourf(xlist= SiO2_dic[i],ylist=Na2O_dic[i])
                if Na2O_Contourf_Result[0]==True:
                    Na2O_plot.contourf(Na2O_Contourf_Result[1], Na2O_Contourf_Result[2], Na2O_Contourf_Result[3], cmap=DensityColorMap, alpha=DensityAlpha)
                    Na2O_plot.contour(Na2O_Contourf_Result[1], Na2O_Contourf_Result[2], Na2O_Contourf_Result[3], colors=DensityLineColor, alpha=DensityLineAlpha)

                K2O_Contourf_Result=self.DrawContourf(xlist= SiO2_dic[i],ylist=K2O_dic[i])
                if K2O_Contourf_Result[0]==True:
                    K2O_plot.contourf(K2O_Contourf_Result[1], K2O_Contourf_Result[2], K2O_Contourf_Result[3], cmap=DensityColorMap, alpha=DensityAlpha)
                    K2O_plot.contour(K2O_Contourf_Result[1], K2O_Contourf_Result[2], K2O_Contourf_Result[3], colors=DensityLineColor, alpha=DensityLineAlpha)

                TiO2_Contourf_Result=self.DrawContourf(xlist= SiO2_dic[i],ylist=TiO2_dic[i])
                if TiO2_Contourf_Result[0]==True:
                    TiO2_plot.contourf(TiO2_Contourf_Result[1], TiO2_Contourf_Result[2], TiO2_Contourf_Result[3], cmap=DensityColorMap, alpha=DensityAlpha)
                    TiO2_plot.contour(TiO2_Contourf_Result[1], TiO2_Contourf_Result[2], TiO2_Contourf_Result[3], colors=DensityLineColor, alpha=DensityLineAlpha)

                P2O5_Contourf_Result=self.DrawContourf(xlist= SiO2_dic[i],ylist=P2O5_dic[i])
                if P2O5_Contourf_Result[0]==True:
                    P2O5_plot.contourf(P2O5_Contourf_Result[1], P2O5_Contourf_Result[2], P2O5_Contourf_Result[3], cmap=DensityColorMap, alpha=DensityAlpha)
                    P2O5_plot.contour(P2O5_Contourf_Result[1], P2O5_Contourf_Result[2], P2O5_Contourf_Result[3], colors=DensityLineColor, alpha=DensityLineAlpha)




        if (self.hyperplane_cb.isChecked()):

            Al2O3_HyperPlane_Result= self.DrawHyperPlane(svm_x = raw.SiO2,svm_y = raw.Al2O3, target_label=raw.Label)
            if Al2O3_HyperPlane_Result[0]==True:
                Al2O3_plot.contourf(Al2O3_HyperPlane_Result[1],Al2O3_HyperPlane_Result[2],Al2O3_HyperPlane_Result[3], cmap='hot', alpha=0.2)

            MgO_HyperPlane_Result= self.DrawHyperPlane(svm_x = raw.SiO2,svm_y = raw.MgO, target_label=raw.Label)
            if MgO_HyperPlane_Result[0]==True:
                MgO_plot.contourf(MgO_HyperPlane_Result[1],MgO_HyperPlane_Result[2],MgO_HyperPlane_Result[3], cmap='hot', alpha=0.2)

            FeTotal_HyperPlane_Result= self.DrawHyperPlane(svm_x = raw.SiO2,svm_y = FeTotal_list, target_label=raw.Label)
            if FeTotal_HyperPlane_Result[0]==True:
                FeTotal_plot.contourf(FeTotal_HyperPlane_Result[1],FeTotal_HyperPlane_Result[2],FeTotal_HyperPlane_Result[3], cmap='hot', alpha=0.2)

            CaO_HyperPlane_Result= self.DrawHyperPlane(svm_x = raw.SiO2,svm_y = raw.CaO, target_label=raw.Label)
            if CaO_HyperPlane_Result[0]==True:
                CaO_plot.contourf(CaO_HyperPlane_Result[1],CaO_HyperPlane_Result[2],CaO_HyperPlane_Result[3], cmap='hot', alpha=0.2)

            Na2O_HyperPlane_Result= self.DrawHyperPlane(svm_x = raw.SiO2,svm_y = raw.Na2O, target_label=raw.Label)
            if Na2O_HyperPlane_Result[0]==True:
                Na2O_plot.contourf(Na2O_HyperPlane_Result[1],Na2O_HyperPlane_Result[2],Na2O_HyperPlane_Result[3], cmap='hot', alpha=0.2)

            K2O_HyperPlane_Result= self.DrawHyperPlane(svm_x = raw.SiO2,svm_y = raw.K2O, target_label=raw.Label)
            if K2O_HyperPlane_Result[0]==True:
                K2O_plot.contourf(K2O_HyperPlane_Result[1],K2O_HyperPlane_Result[2],K2O_HyperPlane_Result[3], cmap='hot', alpha=0.2)

            TiO2_HyperPlane_Result= self.DrawHyperPlane(svm_x = raw.SiO2,svm_y = raw.TiO2, target_label=raw.Label)
            if TiO2_HyperPlane_Result[0]==True:
                TiO2_plot.contourf(TiO2_HyperPlane_Result[1],TiO2_HyperPlane_Result[2],TiO2_HyperPlane_Result[3], cmap='hot', alpha=0.2)

            P2O5_HyperPlane_Result= self.DrawHyperPlane(svm_x = raw.SiO2,svm_y = raw.P2O5, target_label=raw.Label)
            if P2O5_HyperPlane_Result[0]==True:
                P2O5_plot.contourf(P2O5_HyperPlane_Result[1],P2O5_HyperPlane_Result[2],P2O5_HyperPlane_Result[3], cmap='hot', alpha=0.2)






        if len(self.data_to_test)>0:

            LoadedLabels=[]

            Loaded_FeTotal_list = []



            for i in range(len(self.data_to_test)):
                if (self.data_to_test.at[i, 'Label'] in LoadedLabels or self.data_to_test.at[i, 'Label'] == ''):
                    TmpLabel = ''
                else:
                    TmpLabel = self.data_to_test.at[i, 'Label']
                    LoadedLabels.append(TmpLabel)

                Al2O3, MgO, FeO, Fe2O3, CaO, Na2O, K2O, TiO2, P2O5, SiO2 = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
                Al2O3 = self.data_to_test.at[i, 'Al2O3']
                MgO = self.data_to_test.at[i, 'MgO']
                CaO = self.data_to_test.at[i, 'CaO']
                Na2O = self.data_to_test.at[i, 'Na2O']
                K2O = self.data_to_test.at[i, 'K2O']
                TiO2 = self.data_to_test.at[i, 'TiO2']
                P2O5 = self.data_to_test.at[i, 'P2O5']
                SiO2 = self.data_to_test.at[i, 'SiO2']
                if ('FeO' in self.data_to_test.columns.tolist()):
                    FeO = self.data_to_test.at[i, 'FeO']
                if ('Fe2O3' in self.data_to_test.columns.tolist()):
                    Fe2O3 = self.data_to_test.at[i, 'Fe2O3']
                FeTotal = FeO / 72 * 80 + Fe2O3
                if ('TFeO' in self.data_to_test.columns.tolist()):
                    FeTotal = self.data_to_test.at[i, 'TFeO']
                if ('TFe2O3' in self.data_to_test.columns.tolist()):
                    FeTotal = self.data_to_test.at[i, 'TFe2O3']

                Loaded_FeTotal_list.append(FeTotal)



                if (self.show_load_data_cb.isChecked()):

                    Al2O3_plot.scatter(SiO2, Al2O3, marker=self.data_to_test.at[i, 'Marker'],
                                       s=self.data_to_test.at[i, 'Size'], color=self.data_to_test.at[i, 'Color'],
                                       alpha=self.data_to_test.at[i, 'Alpha'], label=TmpLabel)
                    MgO_plot.scatter(SiO2, MgO, marker=self.data_to_test.at[i, 'Marker'],
                                     s=self.data_to_test.at[i, 'Size'], color=self.data_to_test.at[i, 'Color'],
                                     alpha=self.data_to_test.at[i, 'Alpha'], label=TmpLabel)
                    FeTotal_plot.scatter(SiO2, FeTotal, marker=self.data_to_test.at[i, 'Marker'],
                                         s=self.data_to_test.at[i, 'Size'],
                                         color=self.data_to_test.at[i, 'Color'], alpha=self.data_to_test.at[i, 'Alpha'],
                                         label=TmpLabel)
                    CaO_plot.scatter(SiO2, CaO, marker=self.data_to_test.at[i, 'Marker'],
                                     s=self.data_to_test.at[i, 'Size'], color=self.data_to_test.at[i, 'Color'],
                                     alpha=self.data_to_test.at[i, 'Alpha'], label=TmpLabel)
                    Na2O_plot.scatter(SiO2, Na2O, marker=self.data_to_test.at[i, 'Marker'],
                                     s=self.data_to_test.at[i, 'Size'], color=self.data_to_test.at[i, 'Color'],
                                     alpha=self.data_to_test.at[i, 'Alpha'], label=TmpLabel)
                    K2O_plot.scatter(SiO2, K2O, marker=self.data_to_test.at[i, 'Marker'],
                                      s=self.data_to_test.at[i, 'Size'], color=self.data_to_test.at[i, 'Color'],
                                      alpha=self.data_to_test.at[i, 'Alpha'], label=TmpLabel)
                    TiO2_plot.scatter(SiO2, TiO2, marker=self.data_to_test.at[i, 'Marker'],
                                      s=self.data_to_test.at[i, 'Size'], color=self.data_to_test.at[i, 'Color'],
                                      alpha=self.data_to_test.at[i, 'Alpha'], label=TmpLabel)
                    P2O5_plot.scatter(SiO2, P2O5, marker=self.data_to_test.at[i, 'Marker'],
                                      s=self.data_to_test.at[i, 'Size'], color=self.data_to_test.at[i, 'Color'],
                                      alpha=self.data_to_test.at[i, 'Alpha'], label=TmpLabel)



        if (self.show_data_index_cb.isChecked()):

            if 'Index' in self._df.columns.values:

                for i in range(len(self._df)):
                    Al2O3_plot.annotate(self._df.at[i, 'Index'],  xy=(raw.SiO2[i], raw.Al2O3[i]),  color=self._df.at[i, 'Color'], alpha=self._df.at[i, 'Alpha'])
                    MgO_plot.annotate(self._df.at[i, 'Index'],  xy=(raw.SiO2[i], raw.MgO[i]),  color=self._df.at[i, 'Color'], alpha=self._df.at[i, 'Alpha'])
                    FeTotal_plot.annotate(self._df.at[i, 'Index'],  xy=(raw.SiO2[i], FeTotal_list[i]),  color=self._df.at[i, 'Color'], alpha=self._df.at[i, 'Alpha'])
                    CaO_plot.annotate(self._df.at[i, 'Index'],  xy=(raw.SiO2[i], raw.CaO[i]),  color=self._df.at[i, 'Color'], alpha=self._df.at[i, 'Alpha'])
                    Na2O_plot.annotate(self._df.at[i, 'Index'],  xy=(raw.SiO2[i], raw.Na2O[i]),  color=self._df.at[i, 'Color'], alpha=self._df.at[i, 'Alpha'])
                    K2O_plot.annotate(self._df.at[i, 'Index'],  xy=(raw.SiO2[i], raw.K2O[i]),  color=self._df.at[i, 'Color'], alpha=self._df.at[i, 'Alpha'])
                    TiO2_plot.annotate(self._df.at[i, 'Index'],  xy=(raw.SiO2[i], raw.TiO2[i]),  color=self._df.at[i, 'Color'], alpha=self._df.at[i, 'Alpha'])
                    P2O5_plot.annotate(self._df.at[i, 'Index'],  xy=(raw.SiO2[i], raw.P2O5[i]),  color=self._df.at[i, 'Color'], alpha=self._df.at[i, 'Alpha'])


            else:

                for i in range(len(self._df)):
                    Al2O3_plot.annotate('No' + str(i+1),  xy=(raw.SiO2[i], raw.Al2O3[i]),  color=self._df.at[i, 'Color'], alpha=self._df.at[i, 'Alpha'])
                    MgO_plot.annotate('No' + str(i+1),  xy=(raw.SiO2[i], raw.MgO[i]),  color=self._df.at[i, 'Color'], alpha=self._df.at[i, 'Alpha'])
                    FeTotal_plot.annotate('No' + str(i+1),  xy=(raw.SiO2[i], FeTotal_list[i]),  color=self._df.at[i, 'Color'], alpha=self._df.at[i, 'Alpha'])
                    CaO_plot.annotate('No' + str(i+1),  xy=(raw.SiO2[i], raw.CaO[i]),  color=self._df.at[i, 'Color'], alpha=self._df.at[i, 'Alpha'])
                    Na2O_plot.annotate('No' + str(i+1),  xy=(raw.SiO2[i], raw.Na2O[i]),  color=self._df.at[i, 'Color'], alpha=self._df.at[i, 'Alpha'])
                    K2O_plot.annotate('No' + str(i+1),  xy=(raw.SiO2[i], raw.K2O[i]),  color=self._df.at[i, 'Color'], alpha=self._df.at[i, 'Alpha'])
                    TiO2_plot.annotate('No' + str(i+1),  xy=(raw.SiO2[i], raw.TiO2[i]),  color=self._df.at[i, 'Color'], alpha=self._df.at[i, 'Alpha'])
                    P2O5_plot.annotate('No' + str(i+1),  xy=(raw.SiO2[i], raw.P2O5[i]),  color=self._df.at[i, 'Color'], alpha=self._df.at[i, 'Alpha'])





        if (self.legend_cb.isChecked()):
            self.axes[0, 1].legend(bbox_to_anchor=(1.05, 1),loc=2, borderaxespad=0, prop=fontprop)




        self.canvas.draw()


        self.OutPutTitle='Harker'

        self.OutPutFig=self.fig

    def loadDataToTest(self):
        TMP =self.getDataFile()
        if TMP != 'Blank':
            self.data_to_test=TMP[0]
        self.Harker()

    def DrawHyperPlane(self,svm_x=[1,2,3],svm_y =[4,5,6],target_label = [1,1,0]):

        try:

            clf = svm.SVC(C=1.0, kernel='linear', probability=True)
            xx, yy = np.meshgrid(np.arange(min(svm_x), max(svm_x), np.ptp(svm_x) / 500),
                                 np.arange(min(svm_y), max(svm_y), np.ptp(svm_y) / 500))

            le = LabelEncoder()
            le.fit(target_label)
            class_label = le.transform(target_label)
            svm_train = pd.concat([pd.DataFrame(svm_x), pd.DataFrame(svm_y)], axis=1)

            svm_train = svm_train.values
            clf.fit(svm_train, class_label)
            Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])
            Z = Z.reshape(xx.shape)

            return(True,xx, yy, Z)

        except:
            pass
            return(False)

    def DrawContourf(self,xlist=[1,2,3],ylist=[4,5,6]):

        xmin, xmax = min(xlist), max(xlist)
        ymin, ymax = min(ylist), max(ylist)
        # Peform the kernel density estimate
        xx, yy = np.mgrid[xmin:xmax:200j, ymin:ymax:200j]

        positions = np.vstack([xx.ravel(), yy.ravel()])
        values = np.vstack([ xlist,ylist])
        kernelstatus = True
        try:
            st.gaussian_kde(values)
        except Exception as e:
            self.ErrorEvent(text=repr(e))
            kernelstatus = False
            return(False)
        if kernelstatus == True:
            kernel = st.gaussian_kde(values)
            f = np.reshape(kernel(positions).T, xx.shape)
            return(True,xx, yy, f)



    def showPredictResult(self):

        if len(self.data_to_test) > 0:

            df=self.CleanDataFile(self._df)
            df_to_fit=self.Slim(self.CleanDataFile(self.data_to_test))

            clf = svm.SVC(C=1.0, kernel='linear', probability=True)
            le = LabelEncoder()
            le.fit(self._df.Label)
            df_values = self.Slim(df)

            clf.fit(df_values, df.Label)
            Z = clf.predict(np.c_[df_to_fit])
            Z2 = clf.predict_proba(np.c_[df_to_fit])
            proba_df = pd.DataFrame(Z2)
            proba_df.columns = clf.classes_

            proba_list = []
            for i in range(len(proba_df)):
                proba_list.append(round(max(proba_df.iloc[i])+ 0.001, 2))
            predict_result = pd.concat(
                [self.data_to_test['Label'], pd.DataFrame({'SVM Classification': Z}), pd.DataFrame({'Confidence probability': proba_list})],
                axis=1).set_index('Label')
            print(predict_result)

            self.predictAllpop = TableViewer(df=predict_result, title='SVM Predict Result with All Items')
            self.predictAllpop.show()

            '''
            try:
                clf = svm.SVC(C=1.0, kernel='linear',probability= True)
                le = LabelEncoder()
                le.fit(self._df.Label)
                df_values = self.Slim(df)

                clf.fit(df_values, df.Label)
                Z = clf.predict(np.c_[df_to_fit])
                Z2 = clf.predict_proba(np.c_[df_to_fit])
                proba_df = pd.DataFrame(Z2)

                proba_list=[]
                
                for i in range(len(proba_df)):
                    print(proba_df[i])


                proba_df.columns = clf.classes_
                predict_result = pd.concat(
                    [self.data_to_test['Label'], pd.DataFrame({'SVM Classification': Z}), proba_df],
                    axis=1).set_index('Label')
                print(predict_result)

                self.predictAllpop = TableViewer(df=predict_result, title='SVM Predict Result with All Items')
                self.predictAllpop.show()


            except Exception as e:
                msg = 'You need to load another data to run SVM.\n '
                self.ErrorEvent(text= msg +repr(e) )

            '''


