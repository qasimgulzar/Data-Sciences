import matplotlib.pyplot as mp
import numpy

stop_words = ['in','the','of','and','it','you','has','have','may','can','this','other','for','If','if','or','at']


f = open('test4.txt')
allstr = f.readlines()
global_lines = " ".join(allstr).split(" ")
#print(global_lines)
global_lines = [global_lines[i] for i in range(len(global_lines)) if len(global_lines[i]) > 0 and global_lines[i] not in stop_words]
global_line_set = list(set(global_lines))
global_count = [global_lines.count(global_line_set[i]) for i in range(len(global_line_set))]
print(global_line_set)
print(global_count)

glob_dict = zip(global_line_set,global_count)
glob_temp = global_count
glob_temp.sort()
mp.plot(sorted(glob_temp))
mp.xticks(numpy.arange(len(global_line_set)),global_line_set)
mp.show()

print(list(glob_dict))

def temp():
	for l in allstr:
		l = l.replace("."," ")
		l = l.replace(","," ")
		print(l)
		linelist = l.split(" ")
		linelist = [linelist[i] for i in range(len(linelist)) if len(linelist[i]) > 0]
		print(linelist)
		try:
			linelist.remove('')
		except:
			pass 
		countarr = [linelist.count(linelist[i]) for i in range(len(linelist))]
		print(countarr)
