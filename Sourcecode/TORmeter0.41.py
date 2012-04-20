import sys, os;
from Tkinter import *
import tkMessageBox
import tkFileDialog
import datetime

import matplotlib.pyplot as plt
from numpy import *






class EVENT:
    def __init__(self, i_start, player, t0, filename):
        self.i_start, self.player, self.t0, self.filename\
                      = i_start, player, t0, filename;
        self.time = False;
        self.dontmerge = False;

    def dump_data(self, values):
        
        print "%-30s %8s" % (self.mobname, self.t0)
        print "Total time:   %ds" % self.time;
       
        if 'dps' in values:
            print "Average DPS:  %.2f" % self.dps;
        if 'hps' in values:
            print "Average HPS:  %.2f" % self.hps;
        if 'crit' in values:
            print "Crit chance:  %.2f%%" % (self.crit*100) 
        if 'avoid' in values:
            print "Avoidance:    %.2f%%" % (self.avoid*100)
        if 'maxheal' in values:
            self.max_heal[1] = self.replace_words(self.max_heal[1])
            print "Largest heal: %d %s" % (self.max_heal[0], self.max_heal[1])
        if 'maxhit' in values:
            self.max_hit[1] = self.replace_words(self.max_hit[1]);
            print "Largest hit:  %d %s" % (self.max_hit[0], self.max_hit[1])
            
        print "\n";

    def dump_data_new(self):
        output = "%-30s %8s" % (self.mobname, self.t0.split('.')[0])
        output += "\nTotal time:   %ds" % self.time
       

        output += "\n\nAverage DPS:  %.2f" % self.dps

        output += "\nAverage HPS:  %.2f" % self.hps

        output += "\nCrit chance:  %.2f%%" % (self.crit*100) 

        output += "\nAvoidance:    %.2f%%" % (self.avoid*100)

        self.max_heal[1] = self.replace_words(self.max_heal[1])
        output += "\nLargest heal: %d %s" % (self.max_heal[0], self.max_heal[1])

        self.max_hit[1] = self.replace_words(self.max_hit[1]);
        output += "\nLargest hit:  %d %s" % (self.max_hit[0], self.max_hit[1])
            
        return output
        
    def dump_data_file(self, values, outfile):

            outfile.write("%-30s %8s\n" % (self.mobname, self.t0.split('.')[0]))
            outfile.write("Total time:   %ds\n" % self.time)
           
        #if 'dps' in values:
            outfile.write("Average DPS:  %.2f\n" % self.dps)
        #if 'hps' in values:
            outfile.write("Average HPS:  %.2f\n" % self.hps)
        #if 'crit' in values:
            outfile.write("Crit chance:  %.2f%%\n" % (self.crit*100) )
        #if 'avoid' in values:
            outfile.write("Avoidance:    %.2f%%\n" % (self.avoid*100))
        #if 'maxheal' in values:
            self.max_heal[1] = self.replace_words(self.max_heal[1])
            outfile.write("Largest heal: %d %s\n" % (self.max_heal[0], self.max_heal[1]))
        #if 'maxhit' in values:
            self.max_hit[1] = self.replace_words(self.max_hit[1]);
            outfile.write("Largest hit:  %d %s\n" % (self.max_hit[0], self.max_hit[1]))

            outfile.write("\n\n");
            

    def replace_words(self, ability):
        new = ability.replace('Crushed', 'Telekinetic Throw (tick)')
        #add equiv lines here
        return new
        
    def set_endpoint(self, i_end, t_end):
        self.i_end, self.t_end = i_end, t_end;

    def get_arrays(self):
        self.dmg_array = []
        self.dmg_t_array = []
        self.hp_array = []
        self.hp_t_array = []
        
        self.ofile = open(self.filename, 'r')
        i0,iF = self.i_start, self.i_end;
        t0 = self.t0;

        tot_damage = 0;
        tot_healing = 0;
        
        i = 0;
        for line in self.ofile:
            if i in range(i0,iF+1):
                split = line.split('[');
                
                damage = self.get_damage(split);
                healing = self.get_healing(split);
                time = split[1][:-1]
               
                dt = float(self.get_dt(t0,time))
                
                tot_damage += damage;
                self.dmg_array.append(tot_damage)
                self.dmg_t_array.append(dt)
                    
                
                tot_healing += healing;
                self.hp_array.append(tot_healing)
                self.hp_t_array.append(dt)
                    


            i += 1;


        self.hp_t_array = array(self.hp_t_array)
        self.hp_array = array(self.hp_array)
        self.dmg_t_array = array(self.dmg_t_array)
        self.dmg_array = array(self.dmg_array)

        t0_hp = where(self.hp_t_array==0)[0][-1]+1
        t0_dmg = where(self.dmg_t_array==0)[0][-1]+1
        self.hp_array[t0_hp:] = self.hp_array[t0_hp:]/self.hp_t_array[t0_hp:]
        self.dmg_array[t0_dmg:] = self.dmg_array[t0_dmg:]/self.dmg_t_array[t0_dmg:]

        #self.dmg_t_array, self.dmg_array = self.compile_arrays(self.dmg_t_array, self.dmg_array)
        #self.hp_t_array, self.hp_array = self.compile_arrays(self.hp_t_array, self.hp_array)

        
        self.ofile.close();

    def compile_arrays(self, t_vec, vec):
        tmp_vec = []
        tmp_t = []

        for t in t_vec:
            if t not in tmp_t:
                tmp_t.append(t)
                tmp_vec.append(0)
        for i in range(len(tmp_t)):
            ti = tmp_t[i];
            k = 0;
            for j in range(len(t_vec)):
                tj = t_vec[j]
                if tj == ti:
                    tmp_vec[i] += vec[j];
                    k += 1;
            tmp_vec[i] /= float(k)
        return array(tmp_t), array(tmp_vec);
    
    def get_loginfo(self):
        self.ofile = open(self.filename, 'r')
        dt = self.time;
   

        i0,iF = self.i_start, self.i_end;

        tot_damage = 0;
        tot_healing = 0;
        avoided = 0;
        num_hits = 0;
        critted = 0;
        num_attacks = 0;

        max_hit = [0,''];
        max_heal = [0,''];
        
        i = 0;
        for line in self.ofile:
            if i in range(i0,iF+1):
                
                split = line.split('[');
##                if i == 5:
##                    for s in split:
##                        print s
##                    sys.exit(1)
                damage = self.get_damage(split);
                healing = self.get_healing(split);
                avoidance = self.get_avoidance(split);
                crits = self.get_crits(split);

                if damage > max_hit[0]:
                    raw = split[4].split();
                    k = 0;
                    ability = '';
                    while raw[k].startswith('{') == False:
                        ability += raw[k] + " ";
                        k += 1;
                    ability = ability[0:-1];
                    
                    max_hit = [damage, ability]

                if healing > max_heal[0]:
                    raw = split[4].split();
                    k = 0;
                    ability = '';
                    while raw[k].startswith('{') == False:
                        ability += raw[k] + " ";
                        k += 1;
                    ability = ability[0:-1];
                    
                    max_heal = [healing, ability]
                
                tot_damage += damage;
                tot_healing += healing;
                avoided += avoidance[0];
                num_hits += avoidance[1];
                critted += crits[0];
                num_attacks += crits[1];



            i += 1;

        self.ofile.close();
        self.dps = float(tot_damage)/dt;
        self.hps = float(tot_healing)/dt;
        if num_hits != 0:
            self.avoid = float(avoided)/num_hits;
        else:
            self.avoid = 0;
        if num_attacks != 0:
            self.crit = float(critted)/num_attacks;
        else:
            self.crit = 0;
        self.max_hit = max_hit;
        self.max_heal = max_heal;
        

        

    def get_damage(self,split):
        
        damage = 0;
 
        #dealer = player
        if split[2].startswith('@' + self.player):
            #target = non_player
            if split[3].startswith('@' + self.player) == False:   
                for section in split:
                    if "Damage" in section and "FallingDamage" not in section:
                        new_split = section.split()
                        for new_section in new_split:
                            if new_section[0] == "(":
                                raw = new_section.strip('(');
                                damage = int(raw.strip('*'));
                       
    
   
        return damage;

    def get_healing(self,split):
        healing = 0;

        #dealer = player
        if split[2].startswith('@' + self.player):
                for section in split:
                    if "Heal" in section:
                        new_split = section.split()
                        for new_section in new_split:
                            if new_section[0] == "(":
                                raw = new_section.strip('(');
                                healing = int(raw.strip('*)'));

        return healing;

    def get_avoidance(self,split):
     
        if split[2].startswith('@' + self.player) == False and split[3].startswith('@' + self.player):
            if "<1>\n" in split[-1]:
                return [1,1];
            return [0,1];
        return [0,0];
        
    def get_crits(self,split):
        
        if split[2].startswith('@'+self.player) and split[3].startswith('@'+self.player) == False:
            for section in split:
                if "Damage" in section or "Heal" in section:
                    for section1 in split:
                        if "*" in section:
                            return [1,1];
                    return [0,1];
        return [0,0];
    
    def get_total_time(self):
##        split_0 = self.t0.split(':');
##        split_f = self.t_end.split(':');
##
##        factors = [3600,60,1];
##
##        dt = 0;
##        for i in range(3):
##            dt += (int(split_f[i]) - int(split_0[i]))*factors[i];
##        
##        
##
##        return dt;
        return self.get_dt(self.t0, self.t_end)

    def get_dt(self, t1, t2):
        split_0 = t1.split(':');
        split_f = t2.split(':');
        split_f[-1] = split_f[-1].strip(']')
        split_0[-1] = split_0[-1].strip(']')
        
        factors = [3600,60,1];

        dt = 0;
        for i in range(3):
            dt += (float(split_f[i]) - float(split_0[i]))*factors[i];
        
        

        return dt;

    def set_mobname(self, name):
        self.mobname = name;

    def set_totaltime(self):
        self.time = self.get_total_time();
        
    
class TORmeter:
    def __init__(self, master):
        self.filename = "Not given"
        self.values = []
        self.events = None
        self.nofile = True

        menu = Menu(master)
        master.config(menu=menu)

        filemenu = Menu(menu)
        menu.add_cascade(label="File", menu=filemenu)

        self.load = IntVar()
        filemenu.add_command(label="Open log", command=self.openfile)
        filemenu.add_checkbutton(label="Load latest log", variable = self.load, command = self._load)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=master.destroy)

        helpmenu = Menu(menu)
        menu.add_cascade(label="Help", menu=helpmenu)
        helpmenu.add_command(label="README", command=self.openreadme)
        
        
        Label(master, text="Min Enc. time:").grid(row=1, sticky=E + W)
        Label(master, text="Enc. separation threshold:").grid(row=2, sticky=E + W)

        self.e1 = Entry(master)
        self.e2 = Entry(master)
        self.e1.grid(row=1, column=1, sticky = E + W)
        self.e2.grid(row=2, column=1, sticky = E + W)


        self.button = Button(master, text="Analyze", command=self.run)
        self.button.grid(row=4, column=0, sticky = E + W)


        self.dpsPlotButton = Button(master, text="plot DPS", command=self.plotDPS)
        self.hpsPlotButton = Button(master, text="plot HPS", command=self.plotHPS)
        self.dpsPlotButton.grid(row=5, column = 0, sticky = E + W)
        self.hpsPlotButton.grid(row=5, column = 1, sticky = E + W)


        self.writeFileButton = Button(master, text="Write to file", command=self._runToFile)
        self.writeFileButton.grid(row=4, column=1, sticky = E + W)


        #self.load = IntVar()
        #loadbox = Checkbutton(master, text="Load latest file", variable=self.load, command=self._load)
        #loadbox.grid(row=0, column=1, sticky = E + W)

   
        #self.openbutton = Button(master, text="Open Log", command=self.openfile)
        #self.openbutton.grid(row=0, column=0, sticky =E + W)


        self.load_enc = StringVar(master)
        self.load_enc_options = ["Choose Encounter"]
        self.load_enc.set(self.load_enc_options[0])
        self.load_enc_list = apply(OptionMenu, (master, self.load_enc) + tuple(self.load_enc_options))
        self.load_enc_list.grid(row=3, column=0, columnspan=3, sticky= W)

        
        self.load_enc_list['state'] = DISABLED
        self.button['state'] = DISABLED
        self.writeFileButton['state'] = DISABLED

    def openreadme(self):
        os.system("notepad README.txt")

    def plotDPS(self):
        if self.load_enc.get() == "Choose Encounter":
            tkMessageBox.showwarning(
                    "TORmeter",
                    "Please select an encounter."
            )
            return None

        location = self.load_enc_list.cget("text").split()[0]
        for event in self.events:
            time = event.t0.split('.')[0]
            if time == location:
                event.get_arrays();
                plt.plot(event.dmg_t_array, event.dmg_array)
                plt.axis([0,event.dmg_t_array[-1],0,max(event.dmg_array)*1.1])
                plt.title("TORmeter DPS plot")
                plt.xlabel("time")
                plt.ylabel("DPS")
                plt.show()
                
    def plotHPS(self):
        if self.load_enc.get() == "Choose Encounter":
            tkMessageBox.showwarning(
                    "TORmeter",
                    "Please select an encounter."
            )
            return None

        location = self.load_enc_list.cget("text").split()[0]
        for event in self.events:
            time = event.t0.split('.')[0]
            if time == location:
                event.get_arrays();
                plt.plot(event.hp_t_array, event.hp_array)
                plt.axis([0,event.hp_t_array[-1],0,max(event.hp_array)*1.1])
                plt.title("TORmeter HPS plot")
                plt.xlabel("time")
                plt.ylabel("HPS")
                plt.show()


    def change_openbutton_state(self):
        if self.load.get() == 1:
            self.openbutton['state'] = DISABLED
        else:
            self.openbutton['state'] = ACTIVE
            
    def change_enc_state(self):
        if self.var.get() == 1:
            self.load_enc_list['state'] = DISABLED
        else:
            self.load_enc_list['state'] = ACTIVE

    def openfile(self):
        self.filename = tkFileDialog.askopenfilename(title="Choose combatlog to display")
        
        if self.e1.get() == "":
            self.min_t = 0;
        else:
            self.min_t = eval(self.e1.get())
        if self.e2.get() == "":
            self.T_tresh = 0;
        else:
            self.T_tresh = eval(self.e2.get())

        self.events = self.analyze_file();
        self.update_enc_list();
        self.check_filesize();
        self.load.set(0)
        
    def check_filesize(self):
        limit = 30

        
        i = 0
        for event in self.events:
            if event.time > self.min_t:
                i += 1
        if (i > limit):
            tkMessageBox.showwarning(
                "TORmeter",
                "Displaying only 10 latest events (out of %d total).\nTo view details of precurring fights; write to file." % i
        )

    def _load(self):
        #self.change_openbutton_state()
    
        #if self.load.get() == 1:
        cwd = os.getcwd();
        cwd = cwd.strip('TORmeter')
        cwd = cwd[:-1]
        files = os.listdir(cwd);
   

        #filtering logs only
        tray = []
        for log in files:
            if log.startswith("combat") == False:
                tray.append(log)
        for item in tray:
            files.remove(item)
            

        #not counting empty logs
        for log in files:
            if os.path.getsize("../"+log) == 0:
                files.remove(log);

        if len(files) == 0:
            tkMessageBox.showwarning(
                "TORmeter",
                "Found no files to analyze. Make sure you have non-empty logs aviable."
            )
            return None
        
        tmp = [log[12:-11] for log in files];

        for i in range(len(tmp)):
            tmp[i] = tmp[i].replace('-','_');
            tmp[i] = tmp[i].split('_');

        i_max = 0;
        for j in range(5):
            t_max = int(tmp[i_max][j])
        
            for i in range(len(tmp)):
                if tmp[i] != 'old':
                    log = tmp[i];
                    t = int(log[j]);

                    if t < t_max:
                        tmp[i] = 'old';
                    else:
                        i_max = i;
                        t_max = t;
        
        self.filename = "../" + files[i_max];

        if self.e1.get() == "":
            self.min_t = 0;
        else:
            self.min_t = eval(self.e1.get())
        if self.e2.get() == "":
            self.T_tresh = 0;
        else:
            self.T_tresh = eval(self.e2.get())

        self.events = self.analyze_file();
        self.update_enc_list();
        self.check_filesize()
            

    def update_enc_list(self):
        limit = 10
        
        self.load_enc_options = []
        for i in range(len(self.events)):
            if self.events[i].time > self.min_t:
                time = self.events[i].t0.split('.')[0]
                self.load_enc_options.append(time + " " + self.events[i].mobname)
        
        if len(self.load_enc_options) > limit:
            self.load_enc_options = self.load_enc_options[-10:]

        self.load_enc_list["menu"].delete(0, END)
        if len(self.load_enc_options) != 0:
            for i in range(len(self.load_enc_options)):
                self.load_enc_list["menu"].add_command(label=self.load_enc_options[i], command=lambda temp = self.load_enc_options[i]: self.load_enc_list.setvar(self.load_enc_list.cget("textvariable"), value = temp))
            self.load_enc_list['state'] = ACTIVE
            self.button['state'] = ACTIVE
            self.writeFileButton['state'] = ACTIVE
        else:
            tkMessageBox.showwarning(
                "TORmeter",
                "No encounters match your spesified options. Min enc. time too high?"
            )
            self.load_enc_list['state'] = DISABLED
            self.button['state'] = DISABLED
            self.writeFileButton['state'] = DISABLED
            return None
        

        

  
##    def _dps(self):
##        if self.dps.get() == 1: self.values.append('dps')
##        else: self.values.remove('dps')
##        
##        
##    def _hps(self): 
##        if self.hps.get() == 1: self.values.append('hps')
##        else: self.values.remove('hps')
##        
##        
##    def _crit(self):
##        if self.crit.get() == 1: self.values.append('crit')
##        else: self.values.remove('crit')
##        
##        
##    def _avd(self):
##        if self.avd.get() == 1: self.values.append('avoid')
##        else: self.values.remove('avoid')
##        
##        
##    def _maxhit(self):
##        if self.maxhit.get() == 1: self.values.append('maxhit')
##        else: self.values.remove('maxhit')
##        
##        
##    def _maxheal(self):
##        if self.maxheal.get() == 1: self.values.append('maxheal')
##        else: self.values.remove('maxheal')
        

    def run(self):
        if self.load_enc.get() == "Choose Encounter":
            tkMessageBox.showwarning(
                    "TORmeter",
                    "Please select an encounter."
            )
            return None

        location = self.load_enc_list.cget("text").split()[0]
        for event in self.events:
            event_time = event.t0.split(".")[0]
            
            if event_time == location:
                event.get_loginfo();
                text = event.dump_data_new()
                
        tkMessageBox.showinfo(self.load_enc_list.cget("text"), text)
    
    def _runToFile(self):
        events = self.events;
   
        if self.e1.get() == "":
            self.min_t = 0;
        else:
            self.min_t = eval(self.e1.get())
   
        if events == None:
            tkMessageBox.showwarning(
                    "TORmeter",
                    "Please load a file."
            )
            return None

        
        for j in range(len(self.filename)):
            if self.filename[j] == "/":
                i = j;
        filename = self.filename[i+1:-4] + "_out.txt";
        outfile = open(filename, 'w')
        
        for event in events:
            event.get_loginfo();
            if event.time >= self.min_t:
                event.dump_data_file(self.values, outfile);

        outfile.close()
        os.system("notepad " + filename)
                    
         
        
    
    def analyze_file(self):
        name = self.filename
          
        try:
            ofile = open(name,'r')
        except:
            if name == "Not given":
                tkMessageBox.showwarning(
                "TORmeter",
                "Make sure to load a file."
        )
            else:
                tkMessageBox.showwarning(
                "TORmeter",
                "ERROR: Make sure your installation is located correctly in the CombatLogs/TORmeter"
        )   
     
            return None;
    
     
        events=[];
        T_tresh = self.T_tresh 
        i = 0;
        j = 0;
        lock = -1;
        playername = 'INIT';
        mobname = "No Contact Detected";
        time = "lol"
        
        for line in ofile:
            split = line.split();

##            if i == 5:
##                for s in split:
##                    print s
##                sys.exit(1)
                
            #If the line is complete
            if split[-1][-1] == ">" or split[-1][-1] == ")":
                
                check = False;
                check2 = False;

                for piece in split:
                    if 'Damage' in piece and 'FallingDamage' not in piece:
                        check = True;
                    elif 'Heal' in piece:
                        check2 = True;
            

                if 'EnterCombat' in split:
                    
                    playername = split[1].strip('[@')[:-1];
              
                    time = split[0].strip('[')[:-1]
                
                    new_event = EVENT(i,playername,time,name);
                    new_event.mobname = mobname;
                    
                    events.append(new_event);
                    
                #if player is in combat with something besides the player
                elif (split[1].startswith('[@' + playername) and split[2].strip('[@')[:-1] != playername) or (split[2].startswith('[@' + playername) and check == True):
               
                    if ':' not in split[1]:
        
                        if lock != len(events):
                          
                            if (split[2].startswith('[@' + playername) and check == True) and split[1][1] == '@':
                                mobname = split[1].strip('[@')[:-1];
                               # if mobname.startswith("]"):
                                 #   print "hey2"
                                lock = len(events);
                               
      
                            elif  check == True and split[1][1] != '@':
                                mobname = split[1].strip('[') + " ";

                                k = 2
                                while split[k][0] != '{':
                                    mobname += split[k] + " ";
                                    k += 1;
                                #if mobname.startswith("]"):
                                 #   print "hey3"
                                lock = len(events);
                                
                            elif (split[1].startswith('[@' + playername) and split[2].strip('[@')[:-1] != playername) and split[2][1] == '@' and check2 == False:
                                if ':' not in split[2]:
                                    mobname = split[2][2:-1];
                                   # if mobname.startswith("]"):
                                    #    print "hey4"   
                                    lock = len(events);
                            
                            elif (split[1].startswith('[@' + playername) and split[2].startswith('[@' + playername) == False) and split[2][1] != '@' and split[2] != '[]':
                                mobname = split[2].strip('[') + " ";
                                
                                

                                k = 3
                                while split[k][0] != '{':
                                    mobname += split[k] + " ";
                                    k += 1;
                               # if mobname.startswith("]"):
                                 #   print "hey5"

                                lock = len(events);
                    
                          
                        
                            #if mobname.startswith("]"):
                            #    print split
                            

                            events[-1].set_mobname(mobname);
          
                    
                elif 'ExitCombat' in split:
                    time = split[0].strip('[')[:-1]
                    events[-1].set_endpoint(i, time);
                    events[-1].set_totaltime();
             
                i += 1;

        

        for j in range(len(events)):
            if events[j].time == False:
                if j != (len(events)-1):
                    events[j].set_endpoint(events[j+1].i_start, events[j+1].t0);
                    events[j].dontmerge = True;
                    #events[j].mobname += "\n!Unable to determine\ncombat endpoint.!"
                    events[j].set_totaltime();
                else:
                    events[j].set_endpoint(i-1, split[0].strip('[')[:-1])
                    events[j].set_totaltime();
                    
        
        if T_tresh != 0:
            mergelist = [];
            dt = T_tresh+1;
            for i in range(len(events)-1):
##                t1 = events[i].t_end.split(':')
##                t2 = events[i+1].t0.split(':')
##                
##                if int(t1[0])==int(t2[0]):
##                    dt = (float(t2[1])-float(t1[1]))*60 + (float(t2[2]) - int(t1[2]));
                dt = events[0].get_dt(events[i].t_end, events[i+1].t0)
                
                if dt <= T_tresh and events[i].dontmerge == False:
                    if mergelist != []:
                        if mergelist[-1][1] == i:
                            mergelist[-1][1] = i+1
                        else:
                            mergelist.append([i,i+1])
                    else:
                        mergelist.append([i,i+1])

            new_events = []
            for i in range(len(mergelist)):
                start = events[mergelist[i][0]]
                end = events[mergelist[i][1]]
        
                new_event = EVENT(start.i_start, start.player, start.t0, start.filename)
                new_event.set_endpoint(end.i_end, end.t_end)
                new_event.set_totaltime();
                new_event.set_mobname(start.mobname);
                new_events.append(new_event);
            

            tray = []
            for i in range(len(mergelist)):
                merged = mergelist[i];
                events[merged[0]] = new_events[i]
        
                for j in range(merged[0]+1, merged[1]+1):
                    tray.append(j)
              

            tmp = []
            for i in range(len(events)):
                if i not in tray:
                    tmp.append(events[i])
            events = tmp;
            

            
            
        ofile.close();
        return events;



####
root = Tk()
root.title(string="TORmeter")
tormeter = TORmeter(root)
root.mainloop()

