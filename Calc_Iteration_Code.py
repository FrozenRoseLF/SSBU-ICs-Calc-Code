#Copyright 2021 FrozenRose
#SPDX-License-Identifier: Apache-2.0

import  sys, pandas as pd, Move_Data as MD

#Character Data
AD = pd.read_excel(PathToCharacterAttributeData.xlsx, usecols=[0, 1, 2, 3])
Character_DTM = list(AD['Damage Taken'])
Character_KBM = list(AD['KB Received'])
Character_Weights = list(AD['Weight'])
Character_Names = list(AD['Character'])


#Percent from KnockBack Calculator, set Freshness/staleness multiplier (F) and desired knockback.
def KB_Calc(Move_Bd, Move_BKG, Move_KBG, Move_Predamage=0,**kwargs):
    R = kwargs['rage'] if 'rage' in kwargs else 1
    Bd = Move_Bd
    I = kwargs['SH'] if 'SH' in kwargs else 1 #Regular aerials have a multiplier of 1, if SH input 0.85 in kwargs when calling function.
    BKG = Move_BKG
    KBG = Move_KBG
    Predamage = Move_Predamage
    F = 1.05
    Disired_KB = 80

    def Final_Knockback_Needed(KB_Mult):
        KBR = Disired_KB/KB_Mult
        return KBR

    def Damage(DT_Mult, Predamage):
        TD = Bd * I * DT_Mult
        TPD = Predamage * DT_Mult * 1.2
        return TD, TPD

    def Min_Percent(W, Pd):
        P = 0.142857142857143*(-500.0*BKG*R*W - 50000.0*BKG*R - 21.0*ddd*D*Bd*R*F**2*KBG - 49.0*ddd*D*Bd*R*F*KBG - 140.0*ddd*D*R*F*KBG + 500.0*KB*W + 50000.0*KB - 90.0*R*KBG*W - 9000.0*R*KBG)/(ddd*R*KBG*(3.0*Bd*F + 7.0*Bd + 20.0))
        #print(P)
        P -= Pd
        if P < 0:
            P = 0
        #print(P)
        return P

    #Character_Weight_Dictionary = dict(zip(Character_Names, Character_Weights))

    Percent_List = []

    for i in range(0, len(Character_Weights)):
        Kurage = Character_Weights[i]
        Resilience = Character_DTM[i]
        D, Pd = Damage(Resilience, Predamage)
        Stand_Firm = Character_KBM[i]
        if 'Inhaled' in Character_Names[i]:
            ddd = .25
        else: ddd = 1
        KB = Final_Knockback_Needed(Stand_Firm)
        Percent_List.append(Min_Percent(Kurage, Pd))
        #print(Pd, ddd, Character_Names[i], D)

    #For printing or using output in another function
    return Character_Names, Percent_List

    #For outputing to a spreadsheet
    #df = pd.DataFrame(
        #{
        #    "Character":Character_Names,
        #    'Required%':Percent_List,
        #}
     #)

    #df.to_excel(PathToFile, index=False)

#Tumble Doc Calculator. Set Freshness/staleness multiplier (F) and desired knockback
def KB_Calc_Doc(Move_Bd, Move_BKG, Move_KBG, Move_Predamage=0,**kwargs):
    R = kwargs['rage'] if 'rage' in kwargs else 1
    Bd = Move_Bd
    I = kwargs['SH'] if 'SH' in kwargs else 1 #Regular aerials have a multiplier of 1, if SH input 0.85 in kwargs when calling function.
    BKG = Move_BKG
    KBG = Move_KBG
    Predamage = Move_Predamage
    F = 1.05
    Disired_KB = 80
    Move_Type = str(kwargs['Move_Type']) if 'Move_Type' in kwargs else 'None'
    Truncate_Data = kwargs['truncate'] if 'truncate' in kwargs else False
    if Truncate_Data == True: Truncate_Places = ', ' + str(kwargs['Truncate_Places']) + ')'

    def Final_Knockback_Needed(KB_Mult):
        KBR = Disired_KB/KB_Mult
        return KBR

    def Damage(DT_Mult, Predamage):
        TD = Bd * I * DT_Mult
        TPD = Predamage * DT_Mult * 1.2
        return TD, TPD

    def Min_Percent(W, Pd):
        P = 0.142857142857143*(-500.0*BKG*R*W - 50000.0*BKG*R - 21.0*ddd*D*Bd*R*F**2*KBG - 49.0*ddd*D*Bd*R*F*KBG - 140.0*ddd*D*R*F*KBG + 500.0*KB*W + 50000.0*KB - 90.0*R*KBG*W - 9000.0*R*KBG)/(ddd*R*KBG*(3.0*Bd*F + 7.0*Bd + 20.0))
        #print(P)
        P -= Pd
        if P < 0:
            P = 0
        #print(P)
        if Truncate_Data == True:
            P = '=TRUNC(' + str(P) + Truncate_Places
        return P

    #Character_Weight_Dictionary = dict(zip(Character_Names, Character_Weights))

    Percent_List = []

    for i in range(0, len(Character_Weights)):
        if Character_Names[i] == 'Bowser Jr. (Kart)' and Move_Type == 'Throws':
            Percent_List.append('Only hits body')
            continue
        Kurage = Character_Weights[i]
        Resilience = Character_DTM[i]
        D, Pd = Damage(Resilience, Predamage)
        Stand_Firm = Character_KBM[i]
        if 'Inhaled' in Character_Names[i]:
            ddd = .25
        else: ddd = 1
        KB = Final_Knockback_Needed(Stand_Firm)
        Percent_List.append(Min_Percent(Kurage, Pd))
        #print(Pd, ddd, Character_Names[i], D)

    return Character_Names, Percent_List

#Takes in paired moves from Multi_Tumble_Doc, passes them through KB_Calc_Doc, then writes to dataframe.
def Multi_DFWriter(b, c, i, Character_Names, dfShade, tc, tp):
    MR = ' Max Rage'
    NR = ' No Rage'
    print(b, c)
    MT = i[0]
    if i[0] == 'Aerials':
        df = pd.DataFrame(
        {
            #'Character':Character_Names,
            MD.Name_Parser_Notation(b, i[0]) + NR:KB_Calc_Doc(*MD.LP[b], Move_Type=MT, truncate=tc, Truncate_Places=tp)[1] if b !='skip' else 'skip',
            MD.Name_Parser_Notation('SH ' + b, i[0]) + NR:KB_Calc_Doc(*MD.LP[b], SH=.85, Move_Type=MT, truncate=tc, Truncate_Places=tp)[1] if b !='skip' else 'skip',
            MD.Name_Parser_Notation(b, i[0]) + MR:KB_Calc_Doc(*MD.LP[b], rage=1.1, Move_Type=MT, truncate=tc, Truncate_Places=tp)[1] if b !='skip' else 'skip',
            MD.Name_Parser_Notation('SH ' + b, i[0]) + MR:KB_Calc_Doc(*MD.LP[b], SH=.85, rage=1.1, Move_Type=MT, truncate=tc, Truncate_Places=tp)[1] if b !='skip' else 'skip',
            MD.Name_Parser_Notation(c, i[0]) + NR:KB_Calc_Doc(*MD.LP[c], Move_Type=MT, truncate=tc, Truncate_Places=tp)[1] if c !='skip' else 'skip',
            MD.Name_Parser_Notation('SH ' + c, i[0]) + NR:KB_Calc_Doc(*MD.LP[c], SH=.85, Move_Type=MT, truncate=tc, Truncate_Places=tp)[1] if c !='skip' else 'skip',
            MD.Name_Parser_Notation(c, i[0]) + MR:KB_Calc_Doc(*MD.LP[c], rage=1.1, Move_Type=MT, truncate=tc, Truncate_Places=tp)[1] if c !='skip' else 'skip',
            MD.Name_Parser_Notation('SH ' + c, i[0]) + MR:KB_Calc_Doc(*MD.LP[c], SH=.85, rage=1.1, Move_Type=MT, truncate=tc, Truncate_Places=tp)[1] if c !='skip' else 'skip',
            '':'',
            }
        )

    else:
        df = pd.DataFrame(
            {
                #'Character':Character_Names,
                MD.Name_Parser_Notation(b, MT) + NR:KB_Calc_Doc(*MD.LP[b], Move_Type=MT, truncate=tc, Truncate_Places=tp)[1] if b !='skip' else 'skip',
                MD.Name_Parser_Notation(b, MT) + MR:KB_Calc_Doc(*MD.LP[b], rage=1.1, Move_Type=MT, truncate=tc, Truncate_Places=tp)[1] if b !='skip' else 'skip',
                MD.Name_Parser_Notation(c, MT) + NR:KB_Calc_Doc(*MD.LP[c], Move_Type=MT, truncate=tc, Truncate_Places=tp)[1] if c !='skip' else 'skip',
                MD.Name_Parser_Notation(c, MT) + MR:KB_Calc_Doc(*MD.LP[c], rage=1.1, Move_Type=MT, truncate=tc, Truncate_Places=tp)[1] if c !='skip' else 'skip',
                '':'',
                }
            )

    if b == 'skip' or c == 'skip':
        df = df.drop(['skip' + NR, 'skip' + MR], axis=1)
        if i[0] == 'Aerials':
            if '[SH skip]' + NR in df.columns or '[SH skip]' + MR in df.columns: df = df.drop(['[SH skip]' + NR, '[SH skip]' + MR], axis=1)
            if '(SH skip)' + NR in df.columns or '(SH skip)' + MR in df.columns: df = df.drop(['(SH skip)' + NR, '(SH skip)' + MR], axis=1)
    dfShade = pd.concat([dfShade, df], axis=1)
    print(dfShade)
    return dfShade

#Input List Ultra (MD.MoveListAttributes) and truncate keywords. Sorts and pairs moves for Multi_DFWriter, and formats the ending spreadsheet.
def Multi_Tumble_Doc(LU, **kwargs):
    dfl = []
    Category = []
    Loops = 0
    Shadow = pd.DataFrame({'Character':Character_Names})
    tc = kwargs['truncate'] if 'truncate' in kwargs else False
    if tc == True:
        tp = kwargs['Truncate_Places']
    for i in LU:
        print(i)
        Loops +=1
        dfShade = pd.DataFrame({})
        Category.append(i[0])
        #print(Category)
        bitter = [g for g in i[1] if not('Nana' in g)]
        cup = [g for g in i[1] if('Nana' in g)]
        #print(bitter, len(bitter))
        #print(cup, len(cup))
        #print(len(i[1])//2)
        tea = len(bitter) if len(bitter) > len(cup) else len(cup)
        #print(tea)
        for y in range(0, tea):
            b = bitter[y]
            try:
                c = cup[y]
                if c.replace('_Nana', '') != b.replace('_Desynced', ''):
                    if c == 'Fair_Nana_Hitbox_1-3-4':
                        print('Exception, Nana Spike!')
                    elif len(cup) > len(bitter):
                        bitter.insert(y, 'skip')
                        #print(b, c, 'skipped')
                        #print(bitter)
                    elif len(bitter) > len(cup):
                        cup.insert(y, 'skip')
                        #print(b, c, 'skipped')
                        #print(cup)
                    else:
                        bitter.insert(y, 'skip')
                        #print(b,c)
                        #print(bitter, cup)
                        #print('Error')
            except IndexError:
                cup.insert(y, 'skip')
                print('IndexError Occured!', cup)

            b = bitter[y]
            c = cup[y]
            print(bitter, cup)
            dfShade = Multi_DFWriter(b, c, i, Character_Names, dfShade, tc, tp)
        dfShade = pd.concat([Shadow, dfShade], axis=1)
        dfl.append(dfShade)
    dfs = dict(zip(Category, dfl))
    from datetime import date
    today = date.today()
    DateInWords = today.strftime("%B %d, %Y")
    #Change if freshness, sh, or rage multiplier.
    Notes = pd.DataFrame(
        {
            'Calculated with Freshness bonus multiplier of x1.05,':['no rage multiplier of x1 and max rage multiplier of  x1.1,',
                                                                    'shorthop multiplier of .85,',
                                                                    'and move data from KuroganneHammer API accessed ' + DateInWords,
                                                                    '', 'Dependencies that call for recalculations are:',
                                                                    'KuroganneHammer API updating its move data with each new patch and that its syntax/how it stores data remains consistent',
                                                                    '(E.g. The characters it uses to denote hitbox, predamage, etc.)',
                                                                    'Character attribute data, if a character\'s weight, damage taken multiplier, or damage received multipler gets changed',
                                                                    '(Will need to be manually updated in the Character Attribute spreadsheet.)',
                                                                    'Any of the multiplers such as Freshness, rage, or shorthop changing',
                                                                    'Knockback formula changing',
                                                                    '', 'Code to generate by FrozenRose']

            }
        )

    BDU = []
    BKBU = []
    KBGU = []
    PDU = []
    for MoveDataValues in MD.LP.values():
        BDU.append(MoveDataValues[0])
        BKBU.append(MoveDataValues[1])
        KBGU.append(MoveDataValues[2])
        try: PDU.append(MoveDataValues[3])
        except IndexError:
            PDU.append('')


    Move_Data_Used = pd.DataFrame(
        {
            'Move Data':list(MD.LP),
            'Base Damage':BDU,
            'Base Knockback':BKBU,
            'Knockback Growth':KBGU,
            'Pre Damage':PDU,
            '':'',
            }
        )

    Attribute_Data_Used = pd.DataFrame(
        {
            'Character Names':Character_Names,
            'Damage Taken':Character_DTM,
            'Knockback Recieved':Character_KBM,
            'Weight':Character_Weights,
            }
        )
    Data_Used = pd.concat([Move_Data_Used, Attribute_Data_Used], axis=1)
    with pd.ExcelWriter(PathToOutputFile.xlsx) as writertumble:
        workbook = writertumble.book
        format1 = workbook.add_format({'align': 'left', 'bold': True})
        format2 = workbook.add_format({'align': 'left'})
        for sheetname, d in dfs.items():
            d.to_excel(writertumble, sheet_name=sheetname, index=False)
            worksheet = writertumble.sheets[sheetname]
            for idx, col in enumerate(d.columns):
                if col == '':
                    worksheet.set_column(idx, idx, 8.43)
                else: worksheet.set_column(idx, idx, 15)
            for col_num, value in enumerate(d.columns.values):
                worksheet.write(0, col_num, value, format1)
            worksheet.freeze_panes(1,1)
        Notes.to_excel(writertumble, sheet_name='Notes', index=False)
        for col_num, value in enumerate(Notes.columns.values):
            worksheet = writertumble.sheets['Notes']
            worksheet.write(0, col_num, value, format2)
        Data_Used.to_excel(writertumble, sheet_name='Data Used', index=False)
        for col_num, value in enumerate(Data_Used.columns.values):
            worksheet = writertumble.sheets['Data Used']
            worksheet.write(0, col_num, value, format2)
        for idx, col in enumerate(Data_Used.columns):
            if col == '':
                worksheet.set_column(idx, idx, 8.43)
            else: worksheet.set_column(idx, idx, 15)

#Prints Move Names, so you know what to input in *MD.LP['MoveNameHere'].
print(MD.MoveListAttributes)
#Call a function (Calc) with input.

#Multi_Tumble_Doc(MD.MoveListAttributes, truncate=True, Truncate_Places=2)
#KB_Calc(*MD.LP[Jab_1_Hitbox_1-2], SH=1, rage=1)

sys.exit("Inconvience Store")
