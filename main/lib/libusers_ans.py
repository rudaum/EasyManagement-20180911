#!/usr/bin/python
"""
- Purpose:
	Using Ansible as backbone, this library provides functions to
	retrieve a list of users of one or more valid hosts registered
	in the inventory of ansible. This list of users can then be
	parsed to generated excel sheets or as source to Flask

- Author:
	Rudolf Wolter (KN OSY Team)

- Contact for questions and/or comments:
	rudolf.wolter@kuehne-nagel.com

- Version Releases and modifications.
	> 1.0 (30.08.2017) - Initial release with core functionalities.
	> 1.0.1 (12.09.2017) - Implemented 'format_wb' improved 'mksheet'

- TODO:
	Retrieve and place somewhere the last login
	DONE - lsusers not working properly when uising 'user_filter'
"""
### START OF MODULE IMPORTS 
# --------------------------------------------------------------- #
from subprocess import Popen, PIPE
from openpyxl import Workbook
from openpyxl.styles import Border, Side, PatternFill, Font, Alignment
from collections import OrderedDict
# --------------------------------------------------------------- #
### END OF MODULE IMPORTS

### START OF GLOBAL VARIABLES DECLARATION
# --------------------------------------------------------------- #
CONFLICT_COUNTER = 0
WHITE_COLOR = 'FFFFFF'
HEADER_COLOR = '7EA9DE'
SPOT_COLOR = 'D6A6A6'

HEADER_FILL = PatternFill(start_color=HEADER_COLOR, end_color=HEADER_COLOR, fill_type='solid')
ATTR_FILL = PatternFill(start_color=WHITE_COLOR, end_color=WHITE_COLOR, fill_type='solid')
SPOT_FILL = PatternFill(start_color=SPOT_COLOR, end_color=SPOT_COLOR, fill_type='solid')
HEADER_FONT = Font(name='Calibri', size=11, bold=True, color=WHITE_COLOR)
HYPERLINK_FONT = Font(name='Calibri', size=11, underline='single', color='FF0000')
HEADER_BORDER = Border(left=Side(style='thin'),
					   right=Side(style='thin'),
					   top=Side(style='thin'),
					   bottom=Side(style='thin'))

FILENAME = 'em_lsusers.xlsx'
# --------------------------------------------------------------- #
### END OF GLOBAL VARIABLES DECLARATION

### START OF CLASS DEFINITIONS
# --------------------------------------------------------------- #

# --------------------------------------------------------------- #
### END OF CLASS DEFINITIONS

### START OF FUNCTIONS DECLARATION
# --------------------------------------------------------------- #
def debugger(variables):
	print 'Select the Variable you want to inspect:'
	print variables.keys()
	var = raw_input('Selection: ')
	print 'Name:{}, Type: {}'.format(var, type(variables[var]))
	print 'Value: {}'.format(variables[var])
	print ""
# --------------------------------------------------------------- #
# --------------------------------------------------------------- #
def find_in_col(ws, col, search_str):
	for col in ws.iter_cols(min_col=col, max_col=col, max_row=ws.max_row):
		for cell in col:
			if cell.value == search_str:
				return cell
	return False
# --------------------------------------------------------------- #
# --------------------------------------------------------------- #
def find_in_row(ws, row, search_str):
	for row in ws.iter_rows(min_row=row, max_col=ws.max_column, max_row=row):
		for cell in row:
			if cell.value == search_str:
				return cell
	return False
# --------------------------------------------------------------- #
# --------------------------------------------------------------- #
def get_max_col(ws, row):
	max_col = 1
	for col in ws.iter_cols(min_col=2, max_col=8000, min_row=row, max_row=row):
		for cell in col:
			if cell.value is None:
				return max_col
			else:
				max_col += 1
# --------------------------------------------------------------- #
# --------------------------------------------------------------- #
def get_filename():
	global FILENAME
	return FILENAME
# --------------------------------------------------------------- #
# --------------------------------------------------------------- #
def set_filename(name):
	global FILENAME
	FILENAME = name
# --------------------------------------------------------------- #
# --------------------------------------------------------------- #
def order_by_user(raw_users):
	users = OrderedDict()
	for host in raw_users.iterkeys():  # Hostname Level
		for user, attr in raw_users[host]["users"].iteritems():  # User level
			if user not in users:
				users[user] = OrderedDict()
			if host not in users[user]:
				users[user][host] = OrderedDict()
			users[user][host] = attr
	return users
# --------------------------------------------------------------- #

# --------------------------------------------------------------- #
def update_report(wb, user, attr, attr_ref):
	global CONFLICT_COUNTER
	ws = wb.worksheets[0]
	if find_in_col(ws, 1, user) is False:
		targ_row = ws.max_row + 2
		ws.cell(row=targ_row, column=1, value=user)
		ws.cell(row=targ_row, column=1).fill = HEADER_FILL
		ws.cell(row=targ_row, column=1).font = HEADER_FONT

	targ_row = ws.max_row + 1
	CONFLICT_COUNTER += 1
	link_ref = '{}!{}'.format(user,attr_ref)
	conflict = '=HYPERLINK("#{}","Potential conflict spotted for: {}")'.format(link_ref,attr)
	ws.cell(row=targ_row, column=2, value=conflict)
	ws.cell(row=targ_row, column=2).font = HYPERLINK_FONT
	ws.cell(row=targ_row, column=2).fill = SPOT_FILL
# --------------------------------------------------------------- #

# --------------------------------------------------------------- #
def format_wb(wb):
	for sheet_index in range(1, len(wb.sheetnames)):
		ws = wb.worksheets[sheet_index] #getting user's sheet
		ws.column_dimensions['A'].width = 17
		spotted_rows = set()
		for row in range(1, ws.max_row + 1):
			#ws_max_col = get_max_col(ws, row)
			for col in ws.iter_cols(min_row=row, max_row=row, min_col=1, max_col=ws.max_column):
				for cell in col:
					if cell.row is 1 or cell.column is 'A':
						cell.fill = HEADER_FILL
						cell.border = HEADER_BORDER
						cell.font = HEADER_FONT
						if cell.column is not 'A':
							ws.column_dimensions[cell.column].width = 19
					elif cell.row > 1 and cell.column is not 'A':
						cell.fill = ATTR_FILL
						if cell.column is not 'B' :
							# Checking for possible conflicts:
							if cell.value != ws['B' + str(cell.row)].value:
								spotted_rows.add(cell.row) # Adding possible conflict

		# Handling conflicts found
		for row in spotted_rows:
			attr_ref = 'A'+str(row) #setting the attribute's name reference cell
			update_report(wb, ws.title, ws[attr_ref].value, attr_ref) #Updating 'Report' sheet
			for col in ws.iter_cols(min_row=row, max_row=row, min_col=1, max_col=ws.max_column):
				for cell in col:
					cell.fill = SPOT_FILL

	ws = wb.worksheets[0]
	ws.title = 'Report'
	ws['A1'] = '{} Potential Inconsistencies Found:'.format(CONFLICT_COUNTER)
	ws.column_dimensions['A'].width = 15
	ws.column_dimensions['B'].width = 42
	ws.merge_cells('A1:B1')
	ws['A1'].fill = HEADER_FILL
	ws['A1'].border = HEADER_BORDER
	ws['A1'].font = Font(name='Calibri', size=14, bold=True, color=WHITE_COLOR)
	ws['A1'].alignment = Alignment(horizontal='center', vertical='center')
# --------------------------------------------------------------- #
# --------------------------------------------------------------- #

def lsusers(targ_hosts, fulllist=False, user_filter="ALL"):
	"""
	Returns user(s) atributes from the target hosts.
	It contructs an ansible command that is called using subprocess
	module. Then it retrieves a user list with their attributes
	from all target hosts and formats it as Dictionary tree
	"""
	hosts = OrderedDict()


	if fulllist:
		ans_cmd = ["/bin/ansible", "-ba", "lsuser -f " + user_filter]
	else:
		ans_cmd = ["/bin/ansible", "-a", "lsuser -f " + user_filter]
	ans_cmd.append(targ_hosts)

	# Calling Ansible process
	output = Popen(ans_cmd, stdout=PIPE, stderr=PIPE)

	msg_handler = ''

	# Parsing the process output
	for line in output.stdout:
		if " | " in line and "rc=" in line and ">>" in line:  # Parsing hosts line
			hn = line.split(" | ")[0]
			hosts[hn] = OrderedDict()
			hosts[hn]["exec_rc"] = line.split(" | ")[2].split(" ")[0]
			hosts[hn]["exec_msg"] = line.split(" | ")[1]
			hosts[hn]["users"] = OrderedDict()

		# Checking if Ansible could reach/access the host
		# if not, set msg_handler to get the error message in the net line and delete the host's key
		elif '| SUCCESS |' not in line and " | " in line and " => {" in line:  # Parsing Host / Target
			msg_handler = 'HOSTFAIL'
			hn = line.split(" | ")[0]
			hosts[hn] = OrderedDict()
			hosts[hn]["exec_rc"] = line.split(" | ")[1].split(" ")[0]
			hosts[hn]["exec_msg"] = line.split(" | ")[1].split(" ")[0]
			hosts[hn]["users"] = OrderedDict()

		elif ":\n" in line and msg_handler == '':  # Parsing Users Line
			user = line.strip()[:-1]  # stripping ":" from the user
			hosts[hn]["users"][user] = OrderedDict()

		elif "=" in line and msg_handler == '':  # Parsing Attribute
			an = line.strip().split("=", 1)[0]  # attribute's name
			if '_last_' not in an and 'unsuccessful_' not in an:  # Filtering Undesired  attribures
				av = line.strip().split("=", 1)[1].decode('utf-8')  # attribute's value
				hosts[hn]["users"][user][an] = av
		else:
			# Could not reach the server, display the error message and deletes the Key from the dictionary
			if msg_handler == 'HOSTFAIL':
				print 'WARNING! Host {} failed with message: {}'.format(hn, hosts[hn]['exec_msg'])
				del hosts[hn]['exec_rc']
				del hosts[hn]['exec_msg']
				del hosts[hn]['users']
				del hosts[hn]
				msg_handler = ''

	return hosts
# --------------------------------------------------------------- #
# --------------------------------------------------------------- #
def mksheet(raw_users):
	"""
	Builds an excel sheet out from the 'lsusers' function output,
	which comes as a dictionary tree. Then it saves it as a xlsx
	file format
	"""
	users = order_by_user(raw_users)  # formating lsusers raw output
	wb = Workbook()  # creating new workbook
	for user in users.iterkeys():  # Looping over Users
		ws = wb.create_sheet(user)  # Creating user's Tab
		for host in users[user].iterkeys():  # Looping over hosts
			host_col = ws.max_column + 1
			ws.cell(row=1, column=host_col, value=host)  # hostname on 1st row
			ws.cell(row=2, column=1, value="User")  # User name Attribute
			ws.cell(row=2, column=host_col, value=user)  # User name Value
			for attr in users[user][host].iteritems():  # Looping over attributes
				find_attr = find_in_col(ws, 1, attr[0])
				if find_attr is False:
					attr_row = ws.max_row + 1
					ws.cell(row=attr_row, column=1, value=attr[0])  # writting attribute Name
				else:
					attr_row = find_attr.row

				ws.cell(row=attr_row, column=host_col, value=attr[1])  # writting attribute value

	format_wb(wb)
	wb.save(FILENAME)  # saving t=he workbook
	wb.close()
# --------------------------------------------------------------- #
# --------------------------------------------------------------- #
	def mktable_html(raw_users):
		"""
		Builds an html out from the 'lsusers' function output,
		which comes as a dictionary tree. Then it saves it as a html
		file format
		"""
		users = order_by_user(raw_users)  # formating lsusers raw output

		for user in users.iterkeys():  # Looping over Users

			for host in users[user].iterkeys():  # Looping over hosts
				host_col = ws.max_column + 1
				ws.cell(row=1, column=host_col, value=host)  # hostname on 1st row
				ws.cell(row=2, column=1, value="User")  # User name Attribute
				ws.cell(row=2, column=host_col, value=user)  # User name Value
				for attr in users[user][host].iteritems():  # Looping over attributes
					find_attr = find_in_col(ws, 1, attr[0])
					if find_attr is False:
						attr_row = ws.max_row + 1
						ws.cell(row=attr_row, column=1, value=attr[0])  # writting attribute Name
					else:
						attr_row = find_attr.row

					ws.cell(row=attr_row, column=host_col, value=attr[1])  # writting attribute value
		format_wb(wb)
		wb.save(FILENAME)  # saving the workbook
		wb.close()
### END OF FUNCTIONS DECLARATION