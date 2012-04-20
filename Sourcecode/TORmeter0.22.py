import sys, os;

#0.22 notes: Improved output. Option to write to file.


def initialize():
    setupfile = open('DMsettings.txt','r');
    
    for line in setupfile:
        if line.startswith('filename'):
            name = line.split('=')[1].strip();
            if name == 'latest':
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
                    print "Found no files to analyze. Make sure you have non-empty logs aviable."
                    raw_input();
                    sys.exit(1)
                
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
                          
                name = files[i_max];
        
        elif line.startswith('min_time'):
            min_t = int(line.split('=')[1].strip())

        elif line.startswith('values'):
            split = line.split('=')[1].split();
            values = [value.strip(',') for value in split]
        elif line.startswith('new_event_treshold'):
            T_tresh = int(line.split('=')[1].strip())
        elif line.startswith('Vikingstad'):
            print "Vikingstad is %s\n" % line.split('=')[1].strip();
        elif line.startswith('filewrite'):
            filewrite = eval(line.split('=')[1].strip('\n'));
           
            
    setupfile.close();

    return name, min_t, values, T_tresh, filewrite;



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
        
    def dump_data_file(self, values, outfile):

            outfile.write("%-30s %8s\n" % (self.mobname, self.t0))
            outfile.write("Total time: %ds\n" % self.time)
           
            if 'dps' in values:
                outfile.write("Average DPS:  %.2f\n" % self.dps)
            if 'hps' in values:
                outfile.write("Average HPS:  %.2f\n" % self.hps)
            if 'crit' in values:
                outfile.write("Crit chance:  %.2f%%\n" % (self.crit*100) )
            if 'avoid' in values:
                outfile.write("Avoidance:    %.2f%%\n" % (self.avoid*100))
            if 'maxheal' in values:
                self.max_heal[1] = self.replace_words(self.max_heal[1])
                outfile.write("Largest heal: %d %s\n" % (self.max_heal[0], self.max_heal[1]))
            if 'maxhit' in values:
                self.max_hit[1] = self.replace_words(self.max_hit[1]);
                outfile.write("Largest hit:  %d %s\n" % (self.max_hit[0], self.max_hit[1]))

            outfile.write("\n\n");
            

    def replace_words(self, ability):
        new = ability.replace('Crushed', 'Telekinetic Throw (tick)')
        #add equiv lines here
        return new
        
    def set_endpoint(self, i_end, t_end):
        self.i_end, self.t_end = i_end, t_end;

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
        split_0 = self.t0.split(':');
        split_f = self.t_end.split(':');

        factors = [3600,60,1];

        dt = 0;
        for i in range(3):
            dt += (int(split_f[i]) - int(split_0[i]))*factors[i];
        
        

        return dt;

    def set_mobname(self, name):
        self.mobname = name;

    def set_totaltime(self):
        self.time = self.get_total_time();
        
    

def analyze_file(name, T_tresh):
    try:
        ofile = open(name,'r')
    except:
        print "ERROR: Make sure your installation is located correctly in the CombatLogs/TORmeter"
        raw_input();
        sys.exit(1);
        
    events=[];
    i = 0;
    j = 0;
    lock = -1;
    playername = 'INIT';
    mobname = "No Contact Detected";
    time = "lol"
    
    for line in ofile:
        split = line.split();

        #If the line is complete
        if split[-1][-1] == ">" or split[-1][-1] == ")":
            
            check = False;
            for piece in split:
                if 'Damage' in piece:
                    check = True;

            if 'EnterCombat' in split:
                
                playername = split[2].strip('[@')[:-1];
          
                time = split[1].strip(']')
            
                new_event = EVENT(i,playername,time,name);
                new_event.mobname = mobname;
                
                events.append(new_event);
                
            
            #if player is in combat with something besides the player
            elif (split[2].startswith('[@' + playername) and split[3].strip('[@')[:-1] != playername) or (split[3].startswith('[@' + playername) and check == True):
                if ':' not in split[2]:
                    if lock != len(events):
                        if (split[3].startswith('[@' + playername) and check == True) and split[2][1] == '@':
                            mobname = split[2].strip('[@')[:-1];
                        if  check == True and split[2][1] != '@':
                            mobname = split[2].strip('[') + " ";

                            k = 3
                            while split[k][0] != '{':
                                mobname += split[k] + " ";
                                k += 1;
                        if (split[2].startswith('[@' + playername) and split[3].strip('[@')[:-1] != playername) and split[3][1] == '@':
                            mobname = split[3][2:-1];
                        if (split[2].startswith('[@' + playername) and split[3].startswith('[@' + playername) == False) and split[3][1] != '@':
                            mobname = split[3].strip('[') + " ";

                            k = 4
                            while split[k][0] != '{':
                                mobname += split[k] + " ";
                                k += 1;

                        lock = len(events);

                        events[-1].set_mobname(mobname);

                
            elif 'ExitCombat' in split:
                time = split[1].strip(']')
                events[-1].set_endpoint(i, time);
                events[-1].set_totaltime();
         
            i += 1;


    for j in range(len(events)):
        if events[j].time == False:
            if j != (len(events)-1):
                events[j].set_endpoint(events[j+1].i_start, events[j+1].t0);
                events[j].dontmerge = True;
                events[j].mobname += "\n!Unable to determine\ncombat endpoint.!"
                events[j].set_totaltime();
            else:
                events[j].set_endpoint(i-1, split[1].strip(']'))
                events[j].set_totaltime();
                
    
    if T_tresh != 0:
        mergelist = [];
        dt = T_tresh+1;
        for i in range(len(events)-1):
            t1 = events[i].t_end.split(':')
            t2 = events[i+1].t0.split(':')
            
            if int(t1[0])==int(t2[0]):
                dt = (int(t2[1])-int(t1[1]))*60 + (int(t2[2]) - int(t1[2]));
            
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

def main():
    print "SWTOR Damage Meter 1.1 by Skygge@Bloodworthy\n"
    name, min_t, values, T_tresh, filewrite = initialize();
    events = analyze_file("../"+name, T_tresh);

    if filewrite:
        filename = name.strip('.txt') 
        filename = filename.strip('../') + "_out.txt"
        outfile = open(filename, 'w')
        print "Writing data to file: %s" % filename
    
    for event in events:
        event.get_loginfo();
        if event.time >= min_t:
            if filewrite:
                event.dump_data_file(values, outfile);
            else:
                event.dump_data(values);

    if filewrite:
        outfile.close();
        print "File successfully written."
    print "Press [Enter] to exit."

####
main();
raw_input();

