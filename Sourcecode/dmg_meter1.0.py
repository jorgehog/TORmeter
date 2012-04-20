import sys;

namefile = open('DMsettings.txt','r');
for line in namefile:
    if line.startswith('filename'):
        name = line.split('=')[1].strip();
namefile.close();
#name = 'combat_2012-03-17_14_59_05_430465.txt'


class EVENT:
    def __init__(self, i_start, player, t0, filename, label):
        self.i_start, self.player, self.t0, self.filename, self.label\
                      = i_start, player, t0, filename, label;

    def dump_new(self):
        print "Player", self.player ,"combat entry detected at", self.t0 , " [%d]" % self.label;

    def set_endpoint(self, i_end, t_end):
        self.i_end, self.t_end = i_end, t_end;

    def get_dps(self):
        self.ofile = open(self.filename, 'r')
        dt = self.get_total_time();

        i0,iF = self.i_start, self.i_end;

        tot_damage = 0;
        i = 0;
        for line in self.ofile:
            if i in range(i0,iF+1):
                split = line.split('[');
                damage = self.get_damage(split);
                #healing =
                #mob_damage =

                tot_damage += damage;

            i += 1;

        self.ofile.close();
        dps = float(tot_damage)/dt;

        print "Event %d DPS: %g" % (self.label, dps);

    def get_damage(self,split):

        damage = 0;

        #dealer = player
        if split[2][0] == '@':
            
            #target = non_player
            if split[3][0] != '@':
                for section in split:
                    if "Damage" in section:
                        new_split = section.split()
                        for new_section in new_split:
                            if new_section[0] == "(":
                                raw = new_section.strip('(');
                                damage = int(raw.strip('*'));
                       
    
   
        return damage;
    def get_total_time(self):
        split_0 = self.t0.split(':');
        split_f = self.t_end.split(':');

        factors = [3600,60,1];

        dt = 0;
        for i in range(3):
            dt += (int(split_f[i]) - int(split_0[i]))*factors[i];
        
        print 'Total time of encounter %d was %d seconds' % (self.label, dt)

        return dt;
        
    

def analyze_file(name):
    try:
        ofile = open(name,'r')
    except:
        print "ERROR: Make sure your installation is located correctly in the CombatLogs/dist"
        raw_input();
        sys.exit(1);
        
    events=[];
    i = 0;
    j = 0;
    lock = -1;

    for line in ofile:
        split = line.split();
        if 'EnterCombat' in split:
            playername = split[2].strip('[@')[:-1];
            time = split[1].strip(']')

            new_event = EVENT(i,playername,time,name, len(events));
            new_event.dump_new();
            
            events.append(new_event);
        #if player is in combat with something besides the player
        elif split[2].strip('[@')[:-1] == playername and split[3].strip('[@')[:-1] != playername:
            if lock != len(events):
                mobname = split[3].strip('[') + " ";

                k = 4
                while split[k][0] != '{':
                    mobname += split[k] + " ";
                    k += 1;

                lock = len(events);

                print "Fighting: ", mobname, "\n";
            
        elif 'ExitCombat' in split:
            time = split[1].strip(']')
            events[-1].set_endpoint(i, time);
        
        i += 1;

    ofile.close();
    return events;

def pick_event(imax):
    
    try:
        event = input('Select event 0-%d.' % (imax-1));
    except:
        print "Event mismatch."
        event = pick_event(imax);
    if event not in range(imax):
        print "Event mismatch."
        event = pick_event(imax);

    return event;



events = analyze_file("../"+name);
event = pick_event(len(events));
events[event].get_dps();
raw_input();


    
#
