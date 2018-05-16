from random import *

vector_size = 1000;

#boundaries of SRAM memory to inject
#including floor and ceiling for now to avoid having too much empty space
start_addr = 536870912 #0x20000000
end_addr = 537067519 - 32 #0x20030000
# start_ceiling = start_addr + 7000
start_ceiling = start_addr + 1000 #4000 
end_floor = end_addr - 100 #area of the stack to inject in
#end_addr = 536875007 #0x20000fff
addr_count = 0


#boundaries of timer period
start_period = 10
end_period = 24500
some_period = 5000

limit_addrs = False
some_addr = 536871560
some_addr_range = 400

#boundaries of seed
start_seed = 0
end_seed = 1324

#boundaries of bit num
start_bit = 0
end_bit = 7


#clear the vector files before writing new values
with open("vector_addr.txt", "w"):
	pass
with open("vector_period.txt", "w"):
	pass
with open("vector_seed.txt", "w"):
	pass
with open("vector_bit.txt", "w"):
	pass

#open files for writing
addr_file = open("vector_addr.txt","w")
period_file = open("vector_period.txt", "w")
seed_file = open("vector_seed.txt", "w")
bit_file = open("vector_bit.txt", "w") 

if not limit_addrs: 
	while addr_count < vector_size:
		addr = randint(start_addr, end_addr)
		# addr_file.write(hex(addr) + '\n')
		# addr_count = addr_count + 1
		if  addr > end_floor  or addr < start_ceiling:
			addr_file.write(hex(addr) + '\n')
			addr_count = addr_count + 1
else: 
	while addr_count < vector_size:
		addr = randint(some_addr, some_addr + some_addr_range)
		addr_file.write(hex(addr) + '\n')
		addr_count = addr_count + 1

for i in range(vector_size):
	period_file.write(str(randint(start_period, end_period)) + '\n')
	# period_file.write(str(some_period) + '\n')

for i in range(vector_size):
	bit_file.write(str(randint(start_bit, end_bit)) + '\n')

for i in range(vector_size):
	seed_file.write(str(randint(start_seed, end_seed)) + '\n')


addr_file.close() 
period_file.close()
bit_file.close()
seed_file.close()