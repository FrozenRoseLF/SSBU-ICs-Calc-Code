#Copyright 2021 FrozenRose
#SPDX-License-Identifier: Apache-2.0

import json, urllib.request, sys, xlsxwriter, inspect

#Opens json file of ICs move data from KuroganeHammer as a list, then assigns it to a variable. Also dumps it to a file for reading.
with urllib.request.urlopen("https://api.kuroganehammer.com/api/characters/name/IceClimbers/moves?game=ultimate") as url:
    api_data = json.loads(url.read())
    #dump = open(PathToDumpFile,"w+")
    #dump.write(str(api_data))
    #dump.close()
    url.close

#Changes api move name incase characters mess with things, probalby unnecessary.
def Name_Parser(Move_Name):
    Name1 = Move_Name.replace(' ', '_')
    Name2 = Name1.replace('(', '')
    Name3 = Name2.replace(')', '')
    Name4 = Name3.replace(',', '')
    return Name4

#Puts changed api name into sort of ICs notation.
def Name_Parser_Notation(Move_Name, Move_Type):
    Move_Name = Move_Name.replace('_', ' ')
    if Move_Name == 'skip':
        print('Nana shrug')
    elif 'Nana' in Move_Name:
        Move_Name = Move_Name.replace(' Nana', '')
        Move_Name = Move_Name.replace('  ', '')
        if 'Hitbox' in Move_Name:
            d = Move_Name.find('Hitbox')-1
            Move_Name = '(' + Move_Name[0:d] + ')' + Move_Name[d:len(Move_Name)]
        elif 'Hit' in Move_Name:
            d = Move_Name.find('Hit') - 1
            Move_Name = '(' + Move_Name[0:d] + ')' + Move_Name[d:len(Move_Name)]
        else:
            Move_Name = '(' + Move_Name + ')'
    elif 'Nana' not in Move_Name and Move_Type != 'Specials':
        if 'Hitbox' in Move_Name:
            d = Move_Name.find('Hitbox') - 1
            Move_Name = '[' + Move_Name[0:d] + ']' + Move_Name[d:len(Move_Name)]
        elif 'Hit' in Move_Name:
            d = Move_Name.find('Hit') - 1
            Move_Name = '[' + Move_Name[0:d] + ']' + Move_Name[d:len(Move_Name)]
        else:
            Move_Name = '[' + Move_Name + ']'
    elif 'Desynced' in Move_Name:
        Move_Name = Move_Name.replace(' Desynced', '')
        if 'Hitbox' in Move_Name:
            d = Move_Name.find('Hitbox') - 1
            Move_Name = '[' + Move_Name[0:d] + ']' + Move_Name[d:len(Move_Name)]
        elif 'Hit' in Move_Name:
            d = Move_Name.find('Hit') - 1
            Move_Name = '[' + Move_Name[0:d] + ']' + Move_Name[d:len(Move_Name)]
        else:
            Move_Name = '[' + Move_Name + ']'
    elif 'Ice Shot' in Move_Name:
        if 'Hitbox' in Move_Name:
            d = Move_Name.find('Hitbox') - 1
            Move_Name = '[' + Move_Name[0:d] + ']' + Move_Name[d:len(Move_Name)]
        elif 'Hit' in Move_Name:
            d = Move_Name.find('Hit') - 1
            Move_Name = '[' + Move_Name[0:d] + ']' + Move_Name[d:len(Move_Name)]
        else:
            Move_Name = '[' + Move_Name + ']'
    else: print('Popo Shrug')
    print(Move_Name.find('Hitbox'))
    return Move_Name

#For Orginization. Move categories.
class MoveList:
    Tilts = []
    Smashes = []
    Aerials = []
    Jabs = []
    Specials = []
    DashAttacks = []
    Throws = []

#Sorts moves into the categories in class MoveList
def MoveSorter(Nama):
    if 'throw' in Nama:
        MoveList.Throws.append(Nama)
    elif 'Dash_Attack' in Nama:
        MoveList.DashAttacks.append(Nama)
    elif 'Ftilt' in Nama or 'Dtilt' in Nama or 'Utilt' in Nama:
        MoveList.Tilts.append(Nama)
    elif 'smash' in Nama:
        MoveList.Smashes.append(Nama)
    elif 'Uair' in Nama or 'Bair' in Nama or 'Dair' in Nama or 'Nair' in Nama or 'Fair' in Nama:
        MoveList.Aerials.append(Nama)
    elif 'Jab' in Nama:
        MoveList.Jabs.append(Nama)
    else: MoveList.Specials.append(Nama)

#Joins identical hitboxes using reversed dictionary shenanigans.
def HitboxConsolidator(dictionary):
    Rev_dictionary = {}
    New_dictionary = {}
    for k, v in dictionary.items():
        dictionary[k] = tuple(v)
    for key, value in dictionary.items():
        Rev_dictionary.setdefault(value, []).append(key)
    for k, v in Rev_dictionary.items():
        if len(v) > 1:
            J = v[0]
            for i in range(1, len(v)):
                J += '-' + v[i][-1]
        else: J = v[0]
        New_dictionary[J] = list(k)
    return New_dictionary

#Main loop that does everything. Makes a dictionary of move name:base damage, base knockback, knockback growth, pre-damage. Then passes it through to the HitboxConsolidator, and bam a dictionary of move names and data!
LP = {}
Mop = [0]
Janiter = iter(Mop)
#print(Mop)
for i in range(0, len(api_data)):
    #print('start!')
    Staging = {}
    Namae = str(Name_Parser(api_data[i]['Name']))
    if 'Grab' in Namae:
        #print('Grab!')
        #print(i,u)
        continue
    if 'dodge' in Namae:
        #print('Dodge!')
        #print(i,u)
        continue
    if 'Roll' in Namae:
        #print('Roll')
        #print(i,u)
        continue
    for u in Janiter:
        #print(u)
        FD = False
        FB = False
        FK = False
       # print(u, 'Timeloops')
        #print(i, 'the tart')
        LP[Namae] = 'BeHolder'
        if ',' in api_data[i]['BaseDamage']:
            LP[list(LP)[u]] = [float(api_data[i]['BaseDamage'].split(sep=',')[1]),
                float(api_data[i]['BaseKnockBackSetKnockback']),
                float(api_data[i]['KnockbackGrowth']),
                float(api_data[i]['BaseDamage'].split(sep=',')[0])
                ]
            break
        try: MBD = float(api_data[i]['BaseDamage'])
        except ValueError: FD = True
        try: MBK = float(api_data[i]['BaseKnockBackSetKnockback'])
        except ValueError: FB = True
        try: MKB = float(api_data[i]['KnockbackGrowth'])
        except ValueError: FK = True
        if FD == True or FB == True or FK == True:
            MoveNumber = max([api_data[i]['BaseDamage'].count('/'),
                        api_data[i]['BaseKnockBackSetKnockback'].count('/'),
                        api_data[i]['KnockbackGrowth'].count('/')])
            MoveNumber += 1
            for l in range(1, MoveNumber+1):
                Staging[Namae + '_Hitbox_' + str(l)] = 'BeHolder'
            del LP[Namae]
            #print('Gate 1')
            if FD == True:
                HitboxNumber = api_data[i]['BaseDamage'].count('/') + 1
                HitboxNumberList = [n for n in range(0, HitboxNumber)]
                #print(HitboxNumberList)
                if len(HitboxNumberList) < MoveNumber:
                    for o in range(0, MoveNumber - HitboxNumber):
                        HitboxNumberList.append(HitboxNumber - 2)
                for Deaths in range(0, MoveNumber):
                    Lives = HitboxNumberList[Deaths]
                    Staging[list(Staging)[Deaths]] = [float(api_data[i]['BaseDamage'].split(sep='/')[Lives])]
                #print('Gate 2')
            elif FD == False:
                for Deaths in range(0, MoveNumber):
                    Staging[list(Staging)[Deaths]] = [float(api_data[i]['BaseDamage'])]
                #print('Gate 3')
            if FB == True:
                HitboxNumber = api_data[i]['BaseKnockBackSetKnockback'].count('/') + 1
                HitboxNumberList = [n for n in range(0, HitboxNumber)]
                if len(HitboxNumberList) < MoveNumber:
                    for o in range(0, MoveNumber - HitboxNumber):
                        HitboxNumberList.append(HitboxNumber - 2)
                #print('Gate 4')
                for Deaths in range(0, MoveNumber):
                    Lives = HitboxNumberList[Deaths]
                    Staging[list(Staging)[Deaths]].append(float(api_data[i]['BaseKnockBackSetKnockback'].split(sep='/')[Lives]))
            elif FB == False:
                for Deaths in range(0, MoveNumber):
                    Staging[list(Staging)[Deaths]].append(float(api_data[i]['BaseKnockBackSetKnockback']))
                #print('Gate 5')
            if FK == True:
                HitboxNumber = api_data[i]['KnockbackGrowth'].count('/') + 1
                HitboxNumberList = [n for n in range(0, HitboxNumber)]
                if len(HitboxNumberList) < MoveNumber:
                    for o in range(0, MoveNumber - HitboxNumber):
                        HitboxNumberList.append(HitboxNumber - 2)
                for Deaths in range(0, MoveNumber):
                    Lives = HitboxNumberList[Deaths]
                    Staging[list(Staging)[Deaths]].append(float(api_data[i]['KnockbackGrowth'].split(sep='/')[Lives]))
                #print('Gate 6')
            elif FK == False:
                for Deaths in range(0, MoveNumber):
                   Staging[list(Staging)[Deaths]].append(float(api_data[i]['KnockbackGrowth']))
                #print('Gate 7')
            #print(Staging)
            Staging = HitboxConsolidator(Staging)
            LP.update(Staging)
            #print(Staging)
            #print(LP)
            for p in range(1, len(Staging)):
                Mop.append(u+1)
                u = next(Janiter)


        if FD == False and FB == False and FK == False:
            LP[list(LP)[u]] = [float(api_data[i]['BaseDamage']),
                 float(api_data[i]['BaseKnockBackSetKnockback']),
                 float(api_data[i]['KnockbackGrowth'])
                 ]
            #print('Gate f')
        break
    Mop.append(u+1)
    #print(Namae, 'Move Parsed!', LP)
for i in LP:
    MoveSorter(i)
    #print(i)
#print(MoveList.Tilts, MoveList.Smashes, MoveList.Aerials, MoveList.Jabs,
      #MoveList.Specials, MoveList.DashAttacks, MoveList.Throws)

#List Ultra! Gets the categorized moves fram class MoveList and puts it into a list of tuples with lists in them for use in Multi_Tumble_Doc and Multi_DFWriter.
attributes = inspect.getmembers(MoveList, lambda a:not(inspect.isroutine(a)))
MoveListAttributes = [a for a in attributes if not(a[0].startswith('__') and a[0].endswith('__'))]
