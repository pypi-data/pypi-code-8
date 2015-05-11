# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 14:34:22 2015

@author: dominic
"""
import sqlite3, csv, pandas as pd, numpy as np, read
from matplotlib.pyplot import figure, plot, legend, xlabel, ylabel, title, savefig, xlim, ylim, scatter


def make_dino_db():
    conn = sqlite3.connect('dinodata.db')
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS specimens")
    c.execute('''CREATE TABLE IF NOT EXISTS specimens 
                  ( specimen_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    museum TEXT,
                    specimen_number TEXT,
                    description TEXT
                  )''')
    c.execute("DROP TABLE IF EXISTS taxonomy")
    c.execute('''CREATE TABLE IF NOT EXISTS taxonomy 
                  ( taxonomy_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    specimen_id INTEGER,
                    genus TEXT,
                    species TEXT,
                    clade TEXT,
                    grouping TEXT,
                    source INTEGER
                  )''')
    c.execute("DROP TABLE IF EXISTS refs")
    c.execute('''CREATE TABLE IF NOT EXISTS refs 
                  ( ref_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    year TEXT,
                    name TEXT
                  )''')
    c.execute("DROP TABLE IF EXISTS measurements")
    c.execute('''CREATE TABLE IF NOT EXISTS measurements 
                  ( measurement_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    specimen_id INTEGER,
                    measurement_type INTEGER,
                    source INTEGER,
                    value REAL,
                    estimated INTEGER
                  )''')
    c.execute("DROP TABLE IF EXISTS measurement_types")
    c.execute('''CREATE TABLE IF NOT EXISTS measurement_types 
                  ( measurement_type_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    measurement_name TEXT,
                    measurement_abbr TEXT
                  )''')
    c.execute("DROP TABLE IF EXISTS posture")
    c.execute('''CREATE TABLE IF NOT EXISTS posture 
                  ( specimen_id INTEGER,
                    posture TEXT
                  )''')
    with open('limb_dimensions.csv', 'rb') as csvfile:
        limbdata = csv.reader(csvfile, delimiter=',', quotechar='|')
        for idx, row in enumerate(limbdata):
            if idx == 0:
                col_num = len(row)
                first_meas = row.index('F R L')
                print col_num, first_meas
                start_id = 0
                while start_id + first_meas < first_meas+26:
                    query = "INSERT INTO measurement_types(measurement_abbr) VALUES ('"+row[start_id+first_meas]+"')"
                    c.execute(query)
                    start_id = start_id + 1
                first_meas = row.index('F R L')
                mus = row.index('Museum')
                spec_no = row.index('Specimen')
                clade = row.index('Clade')
                posture = row.index('Posture')
                genus = row.index('Genus')
                grouping = row.index('Grouping')
            else:
                if row[mus] and row[spec_no]:
                    print (row[mus], row[spec_no])
                    print row
                    existing = c.execute("SELECT specimen_id FROM specimens WHERE museum=? AND specimen_number=?", (row[mus], row[spec_no])).fetchall()
                    if len(existing) == 0:
                        c.execute("INSERT INTO specimens(museum, specimen_number) VALUES(?, ?)", (row[mus],row[spec_no]))
                        specimen_id = c.lastrowid
                        genus_value = row[genus]
                        if genus_value == '':
                            genus_value = '?'
                        grouping_value = row[grouping]
                        if grouping_value == '':
                            grouping_value = '?'
                        c.execute("INSERT INTO taxonomy(specimen_id, genus, clade, grouping) VALUES(?, ?, ?, ?)", (specimen_id, genus_value, row[clade], grouping_value))
                    else:
                        specimen_id = existing[0][0]
                    c.execute("INSERT INTO  posture(specimen_id, posture) VALUES(?, ?)", (specimen_id, row[posture]))
                    c.execute("SELECT specimen_id FROM specimens WHERE museum=? AND specimen_number=?", (row[mus], row[spec_no]))
                    specimen_id = c.fetchone()[0]
                    for count, meas in enumerate(row[first_meas:first_meas+26]):
                        if meas:
                            try:
                                numerical_val = float(meas)
                                c.execute("INSERT INTO measurements(specimen_id, measurement_type, value) VALUES(?, ?, ?)", (specimen_id, count+1, numerical_val))
                            except ValueError:
                                pass # do nothing
    c.execute("SELECT COUNT(*) FROM measurements" )
    print "Number of measurements", c.fetchone()
    conn.commit()
    conn.close()

def get_meas(specimen_id, cols, c):
    vals = []
    for col in cols:
        c.execute("SELECT value FROM measurements WHERE specimen_id="+str(specimen_id)+" AND measurement_type="+str(col))
        for row in c.fetchall():
            vals.append(row[0])
    if vals:
        return sum(vals)/(float(len(vals)))
    else:
        return None

def get_summary_meas(specimen_id, c, est_params=None):
    summary = {}
    summary['fl'] = get_meas(specimen_id, [1,2,3], c)
    summary['fcirc'] = get_meas(specimen_id, [13,14,15], c)
    summary['fapw'] = get_meas(specimen_id, [4,5,6], c)
    summary['fmlw'] = get_meas(specimen_id, [7,8,9], c)
    if est_params!=None:
        if summary['fcirc']==None and summary['fmlw']!= None:
            summary['fcirc']=est_params['fem_mlw'][0]*summary['fmlw']+est_params['fem_mlw'][1]
    summary['fw'] = get_meas(specimen_id, [10,11,12], c)
#    if est_params!=None:
#        if summary['fcirc']==None and summary['fw']!= None:
#            summary['fcirc']=2.487*summary['fw']+27.294
    summary['hl'] = get_meas(specimen_id, [16,17,18], c) # Humerus length
    summary['hcirc'] = get_meas(specimen_id, [24,25,26], c)
    summary['hapw'] = get_meas(specimen_id,[19], c)
    summary['hmlw'] = get_meas(specimen_id,[20], c)
    if est_params!=None:
        if summary['hcirc']==None and summary['hmlw']!=None:
            summary['hcirc']= est_params['hum_mlw'][0]*summary['hmlw'] + est_params['hum_mlw'][1]
    summary['hw'] = get_meas(specimen_id,[21,22,23], c)
#    if est_params!=None:
#        if summary['hcirc']==None and summary['hw']!=None:
#            summary['hcirc']=2.655*summary['hw']+12.671
    return summary

def get_all_data(est=None):
    conn = sqlite3.connect('/home/dominic/Dropbox/Thesis/1 Postcranial evolution/analyses/2015 Spring limb analyses/dinodata.db')
    c = conn.cursor()
    
    ### GET ALL OBSERVATIONS FOR ALL SPECIMENS
    db_taxa = c.execute("SELECT * FROM specimens").fetchall()
    rows_list = []
    x = 0
    for row in db_taxa:
        if x%100==0:
            print x, 'of', len(db_taxa)
        c.execute("SELECT COUNT(*) FROM measurements WHERE specimen_id="+str(row[0]))
        if c.fetchone()[0] > 0:
            measurements = get_summary_meas(row[0], c, est_params=est)
            tax_info = c.execute("SELECT genus, clade, grouping FROM taxonomy WHERE specimen_id="+str(row[0])).fetchall()
            genus = tax_info[0][0].strip()
            clade = tax_info[0][1]
            grouping = tax_info[0][2]
            postures = c.execute("SELECT posture FROM posture WHERE specimen_id="+str(row[0])).fetchall()
            posture = 'indet'
            for suggestion in postures:
                if suggestion[0] != '':
                    posture=suggestion[0]
            measurements.update({'genus':genus, 'specimen':row[1]+' '+row[2], 'clade':clade, 'grouping':grouping, 'posture':posture})
            rows_list.append(measurements)
        x = x+ 1
    df = pd.DataFrame(rows_list)
    c.close()
    return df

def main_analysis(df): # Takes a dataframe of all observations
    
    ### SUMMARIZE INTO ONE OBSERVATION FOR EACH SPECIMEN JUST FOR SPECIMENS
    ### WHERE ALL MEASUREMENTS WHERE ORIGINALLY PRESENT
    all_taxa=[]
    for row in xrange(0,len(df)):
        if df.iloc[row,:]['genus'] not in all_taxa:
            all_taxa.append(df.iloc[row,:]['genus'])
    print all_taxa
#    complete_rows = []
    complete_rows=[['Genus','clade','posture','fcirc','fl','hcirc','hl']]
    for taxon in all_taxa:
        subset = df[df['genus']==taxon]
        subset.sort(columns='specimen')
        orig_subset = subset[((subset['fl']>0)&(subset['fcirc']>0)&(subset['hl']>0)&(subset['hcirc']>0))]    
        if len(orig_subset) > 0:
            if len(orig_subset)>1:
                max_fl = max(orig_subset['fl'])
                big_idx = np.where(orig_subset['fl']==max_fl)[0][0]
                biggest = orig_subset.iloc[big_idx,]
            else:
                biggest=orig_subset.iloc[0,]
            complete_rows.append([str(biggest['genus']),str(biggest['clade']),str(biggest['posture']),float(biggest['fcirc']),float(biggest['fl']),float(biggest['hcirc']),float(biggest['hl'])]) 
    for row in complete_rows:
        print row
    all_complete=pd.DataFrame(complete_rows[1:])
    all_complete.columns = complete_rows[0]
    print all_complete.head()
    print len(all_complete),'taxa have all 4 measurements'
    
    ### EXAMINE DATA
    fignum = 1
    figure(fignum)
    ornith_strict=all_complete[all_complete['clade']=='Ornithischia']
    thero_strict=all_complete[all_complete['clade']=='Theropoda']
    sauro_strict=all_complete[all_complete['clade']=='Sauropodomorpha']
    scatter(ornith_strict['fcirc'],ornith_strict['hcirc'], c='b', label='Ornithischians')
    scatter(thero_strict['fcirc'],thero_strict['hcirc'], c='r', label='Theropods')
    scatter(sauro_strict['fcirc'],sauro_strict['hcirc'], c='g', label='Sauropods')
    xlabel('Femoral circumference')
    ylabel('Humeral circumference')
    title('F:H ratio in dinosaurs, complete only')
    legend()
    savefig('/home/dominic/Dropbox/Thesis/1 Postcranial evolution/analyses/2015 Spring limb analyses/figures/Fig'+str(fignum)+'_F-H_ratio_by_clade.svg')
    fignum=fignum+1
    figure(fignum)
    biped_strict=all_complete[all_complete['posture']=='Bipedal']
    quad_strict=all_complete[all_complete['posture']=='Quadrupedal']
    scatter(biped_strict['fcirc'],biped_strict['hcirc'], c='b', label='Bipeds')
    scatter(quad_strict['fcirc'],quad_strict['hcirc'], c='r', label='Quadrupeds')
    xlabel('Femoral circumference')
    ylabel('Humeral circumference')
    title('F:H ratio in dinosaurs, complete only')
    legend()
    
    ### REGRESSION OF CIRCUMFERENCE IN DIFFERENT CLADES
    regb = biped_strict[((biped_strict.fcirc>0)&(biped_strict.hcirc>0))]
    A_biped=np.c_[np.array(regb.fcirc), np.ones(len(regb.fcirc))]
    m_biped, c_biped = np.linalg.lstsq(A_biped, np.array(regb.hcirc))[0]
    print 'Bipeds: slope',m_biped,'intercept',c_biped
    plot(regb.fcirc, m_biped*np.array(regb.fcirc)+c_biped, 'blue')
    regq = quad_strict[((quad_strict.fcirc>0)&(quad_strict.hcirc>0))]
    A_quad=np.c_[np.array(regq.fcirc), np.ones(len(regq.fcirc))]
    m_quad, c_quad = np.linalg.lstsq(A_quad, np.array(regq.hcirc))[0]
    print 'Quadrupeds: slope',m_quad,'intercept',c_quad
    plot(regq.fcirc, m_quad*np.array(regq.fcirc)+c_quad, 'red')
    ylim(0,700)
    savefig('/home/dominic/Dropbox/Thesis/1 Postcranial evolution/analyses/2015 Spring limb analyses/figures/Fig'+str(fignum)+'_F-H_ratio_by_posture_with_regression.svg')
    
    ### CALCULATE CIRCUMFERENCE ESTIMATION REGRESSIONS FROM FULL
    fem_subset = df[((df['fmlw']>0)&(df['fcirc']>0))]    
    hum_subset = df[((df['hmlw']>0)&(df['hcirc']>0))]    
    
    A_femur=np.c_[np.array(fem_subset.fmlw), np.ones(len(fem_subset.fmlw))]
    m_femur, c_femur = np.linalg.lstsq(A_femur, np.array(fem_subset.fcirc))[0]
    print 'Femur estimation params',m_femur, c_femur
    A_humerus=np.c_[np.array(hum_subset.hmlw), np.ones(len(hum_subset.hmlw))]
    m_humerus, c_humerus = np.linalg.lstsq(A_humerus, np.array(hum_subset.hcirc))[0]
    print 'Humerus estimation params',m_humerus, c_humerus
    circ_est_params={'fem_mlw':[m_femur, c_femur], 'hum_mlw':[m_humerus, c_humerus]}
    
    df_all = get_all_data(est=circ_est_params)
    
    all_taxa=[]
    for row in xrange(0,len(df_all)):
        if df_all.iloc[row,:]['genus'] not in all_taxa:
            all_taxa.append(df_all.iloc[row,:]['genus'])
    print all_taxa
    circ_est_params={'fem':[m_femur, c_femur], 'hum':[m_humerus, c_humerus]}
    all_limb_rows=[['Genus','clade','posture','fcirc','fl','hcirc','hl']]
    for taxon in all_taxa:
        subset = df_all[df_all['genus']==taxon]
        subset.sort(columns='specimen')
        orig_subset = subset[((subset['fl']>0)&(subset['fcirc']>0)&(subset['hl']>0)&(subset['hcirc']>0))]    
        if len(orig_subset) > 0:
            if len(orig_subset)>1:
                max_fl = max(orig_subset['fl'])
                big_idx = np.where(orig_subset['fl']==max_fl)[0][0]
                biggest = orig_subset.iloc[big_idx,]
            else:
                biggest=orig_subset.iloc[0,]
            all_limb_rows.append([str(biggest['genus']),str(biggest['clade']),str(biggest['posture']),float(biggest['fcirc']),float(biggest['fl']),float(biggest['hcirc']),float(biggest['hl'])]) 
    for row in all_limb_rows:
        print row
    all_comp_incomp=pd.DataFrame(all_limb_rows[1:])
    all_comp_incomp.columns = all_limb_rows[0]
    print all_comp_incomp.head()
    print len(all_comp_incomp),'taxa have all 4 measurements'
    
    
    fignum=fignum+1
    figure(fignum)
    ornith_strict=all_comp_incomp[all_comp_incomp['clade']=='Ornithischia']
    thero_strict=all_comp_incomp[all_comp_incomp['clade']=='Theropoda']
    sauro_strict=all_comp_incomp[all_comp_incomp['clade']=='Sauropodomorpha']
    scatter(ornith_strict['fcirc'],ornith_strict['hcirc'], c='b', label='Ornithischians')
    scatter(thero_strict['fcirc'],thero_strict['hcirc'], c='r', label='Theropods')
    scatter(sauro_strict['fcirc'],sauro_strict['hcirc'], c='g', label='Sauropods')
    xlabel('Femoral circumference')
    ylabel('Humeral circumference')
    title('F:H ratio in dinosaurs, complete only')
    legend()
    savefig('/home/dominic/Dropbox/Thesis/1 Postcranial evolution/analyses/2015 Spring limb analyses/figures/Fig'+str(fignum)+'_F-H_ratio_by_clade_inc_estimated.svg')
    fignum=fignum+1
    figure(fignum)
    biped_strict=all_comp_incomp[all_comp_incomp['posture']=='Bipedal']
    quad_strict=all_comp_incomp[all_comp_incomp['posture']=='Quadrupedal']
    scatter(biped_strict['fcirc'],biped_strict['hcirc'], c='b', label='Bipeds')
    scatter(quad_strict['fcirc'],quad_strict['hcirc'], c='r', label='Quadrupeds')
    xlabel('Femoral circumference')
    ylabel('Humeral circumference')
    title('F:H ratio in dinosaurs, complete only')
    legend()
    savefig('/home/dominic/Dropbox/Thesis/1 Postcranial evolution/analyses/2015 Spring limb analyses/figures/Fig'+str(fignum)+'_F-H_ratio_by_posture_inc_estimated.svg')
    
    for row in xrange(0,len(biped_strict)):
        if (biped_strict.iloc[row,:]['fcirc']/biped_strict.iloc[row,:]['hcirc']) < 0.5:
            print biped_strict.iloc[row,:]['Genus']
    
    #Regress against FL by clade -> with and without estimation
    #PGLS of ratio vs FL on tree -> correlation?
    return all_comp_incomp

def nx_to_newark_with_branch_lengths(int_node, tree):
    descens = tree.successors(int_node)
    if len(descens) == 0:
        predes = tree.predecessors(descens[0])
        return "(" + str(tree.node[int_node]['name']) + ":" + str(tree.edge[predes][int_node]["length"]) + ")"
    if tree.degree(descens[0])==1 and tree.degree(descens[1]) == 1:
        return "(" + str(tree.node[descens[0]]['name']) + ":" + str(tree.edge[int_node][descens[0]]["length"]) + "," + str(tree.node[descens[1]]['name']) + ":" + str(tree.edge[int_node][descens[1]]["length"]) + ")"
    else:
        text = []
        for tip in descens:
            if tree.degree(tip) == 1:
                text.append(str(tree.node[tip]['name']) + ":" + str(tree.edge[int_node][tip]["length"]) )
            else:
                text.append(nx_to_newark_with_branch_lengths(tip,tree)  + ":" + str(tree.edge[int_node][tip]["length"]) )
        return "(" + text[0] + "," + text[1] + ")"

def make_tree(tips_to_include):
    ts = read.read_trees('/home/dominic/Dropbox/Thesis/1 Postcranial evolution/analyses/2015 Spring limb analyses/Benson14_Dinosauria_tree_edited.txt')
    t=ts[0]
    taxon_names = t.tip_names()
    for taxon in taxon_names:
        to_drop = ['IGM','Minotaurasaurus','Elrhazosaurus','Cedarorestes',
                   'Tanius','Pampdromaeus','Skayentakatae',
                   'Chuandongocoelurus','Piatnizkysaurus','Piveaeausaurus',
                   'CV','Dromiceomimus','Huixagnathus','Rinchenia','Ingenia',
                   'Enigmosaurus','Zanzabazaar','Makhala','Adasaurus',
                   'Jixianornis','Galveosaurus', 'French',]
        for dropped in to_drop:
            if dropped in taxon:
                print 'dropping', taxon
                t.drop_tip(taxon)
    taxon_names = t.tip_names()
    print len(taxon_names)
    f=open('/home/dominic/Dropbox/Thesis/1 Postcranial evolution/analyses/2015 Spring limb analyses/make scaled tree/ages1.csv')
    csvfile = csv.reader(f)
    age_dict = {}
    for row in csvfile:
        print row
        age_dict[row[0].replace(' ','_')]=[float(row[1]), float(row[2])]
    t.timescale(age_dict)
    for edge in t.edges():
        print edge, t.edge[edge[0]][edge[1]]["length"]
#    print sorted(t.tip_names())
#    print nx_to_newark_with_branch_lengths(t.root(), t)    
    
    print t.is_timescaled()
    meas_taxa = []
    taxa_left = []
    for row in xrange(0,len(tips_to_include)):
        meas_taxa.append(tips_to_include.iloc[row,:]['Genus'])
        taxa_left.append(tips_to_include.iloc[row,:]['Genus'])
    taxon_dict={}
    for tip in t.tip_keys():
        if '_' in t.node[tip]['name']:
            pos = t.node[tip]['name'].index('_')
            new_name = t.node[tip]['name'][:pos]
            t.node[tip]['name'] = new_name
        taxon_dict[tip] = t.node[tip]['name']
    print '\n\n', t.tip_keys()
    print '\n\n', t.edges()
    for tip in t.tip_keys():
        if taxon_dict[tip] not in taxa_left:
#            print tip, t.node[tip]['name'], taxon_dict[tip]
            while True:
                if taxon_dict[tip] in t.tip_names():
#                    print ' ',taxon_dict[tip]
                    t.drop_tip(t.node[tip]['name'])
                else:
                    break
        else:
            print taxon_dict[tip]
            taxa_left = taxa_left[:taxa_left.index(t.node[tip]['name'])]+taxa_left[taxa_left.index(t.node[tip]['name'])+1:]
    for taxon in taxa_left:
        meas_taxa = meas_taxa[:meas_taxa.index(taxon)] + meas_taxa[meas_taxa.index(taxon)+1:]
    matching_data = [] 
    print tips_to_include.head()
    for taxon in meas_taxa:
        print taxon
        fcirc = float(tips_to_include[tips_to_include['Genus']==taxon]['fcirc'])
        hcirc = float(tips_to_include[tips_to_include['Genus']==taxon]['hcirc'])
        fl = float(tips_to_include[tips_to_include['Genus']==taxon]['fl'])
        matching_data.append({'Genus':taxon, 'fcirc':fcirc, 'hcirc':hcirc, 'fl':fl})
    output_df = pd.DataFrame(matching_data)
    print t.is_timescaled()
    
    f = open('final_tree.tre', 'w')
    f.write(nx_to_newark_with_branch_lengths(t.root(), t))
    f.close()
    print output_df
    output_df.to_csv('final_data.csv')
    
    return nx_to_newark_with_branch_lengths(t.root(), t), output_df

#Uncomment to create database
#make_dino_db()
#orig_data=get_all_data()
#all_data = main_analysis(orig_data)


pared_tree, pared_data = make_tree(all_data)



#Anatotitan
#Dryosaurus
#Probactrosaurus
#Wannanosaurus
#Aucasaurus
#Acrocanthosaurus
#Lesothosaurus
#Piatnitzkysaurus
#Ceratosaurus

