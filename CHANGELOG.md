[V_1.0, 05.04.2020]
1.	Amazing_race.py
    a.	Changed multithreading to multiprocessing, to utilize multiple CPU cores  
    b.	Fixed bug when integer was read as float  
c.	Fixed bug when average speed was calculated incorrectly   
d.	Moved progress printer into a separate class and use it as shared (memory) object with different processes.   
e.	Renamed function summarize_data into summarize_data_for_batch    
f.	Added example how to run __main__   
g.	Reorganised imports    
h.	Cleaned code and style    
i.	Added comments and document blocks    
2.	Partial_summary.py    
a.	Added method add_new_data and add_new_leg for adding new leg data to summary    
b.	Removed function avg_speed and integrated it inline inside add_new_data    
c.	Moved combine_pair into utils.py    
d.	Cleaned code and style    
e.	Added comments and document blocks    
3.	Custom_exceptions.py    
a.	Created file with exceptions, added new custom exception    
4.	ProgressMonitor.py    
a.	Created shared memory object ProgressMonitor for monitoring progress    
b.	Fixed method for reporting progress every 5%    
c.	Secured method to be safe for multithreading    
5.	Utils.py    
a.	Moved method from partial_summary#combine_pair into utils    
b.	Added method round_progress to utils    
c.	Added comments, cleaned style.    
