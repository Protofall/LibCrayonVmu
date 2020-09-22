# Needed so we can use scons stuff like builders
from SCons.Script import *

def create_builders(our_vars):
	env = list()
	env.append(
		Environment(
			ENV = os.environ,
			CC = 'kos-cc',
			CXX = 'kos-c++',
			AR = 'kos-ar',
		)
	)

	env[-1]['PLATFORMS'] = 'dreamcast'

	# Making sure we use the right prefix and suffix
	env[-1]['LIBPREFIX'] = 'lib'
	env[-1]['LIBSUFFIX'] = '.a'
	env[-1]['OBJSUFFIX'] = '.o'	# Windows has .obj
	env[-1]['PROGSUFFIX'] = '.elf'

	# Fix this later, here's a hack for now
	env[-1]['KOS_BASE'] = env[-1]['ENV']['KOS_BASE']
	env[-1]['KOS_GENROMFS'] = env[-1]['ENV']['KOS_GENROMFS']

	# Location of IP.BIN
	if 'IP_BIN_DIR' in our_vars:
		env[-1]['IP_BIN_DIR'] = our_vars['IP_BIN_DIR'] + 'IP.BIN'

	# Add the platform
	env[-1]['SPECIFIC_PLATFORM'] = 'dreamcast'

	colour_version = [4, 9, 0]

	# Set some env vars for all envs
	for e in env:
		# Ensure CRAYON_SF_BASE is set
		if 'CRAYON_SF_BASE' in our_vars:
			e['CRAYON_SF_BASE'] = our_vars['CRAYON_SF_BASE']
			# e.AppendUnique(CPPPATH = ['$CRAYON_SF_BASE'])	# Doesn't seem to be nessisary, but keeping just incase
			e.AppendUnique(CPPPATH = ['$CRAYON_SF_BASE/include/'])
		else:
			print('CRAYON_SF_BASE is missing, please add the path')
			Exit(1)

		e['CODE_DIR'] = 'src'
		e['CDFS_DIR'] = 'cdfs'
		if 'PROG_NAME' in our_vars:
			e['PROG_NAME'] = our_vars['PROG_NAME']

		#Add in some cflags if in debug mode
		if False == True:
			# Wformat level 2 has extra checks over standard.
			# no-common is where two files define the same global var when they should be seperate
			# g3 is like g, but it includes macro information
			e.AppendUnique(CPPFLAGS = ['-g3', '-Wall', '-Wformat=2', '-fno-common'])

		# Enables GCC colour (Since it normally only does colour for terminals and scons is just an "output")
		# Major, Minor, Patch version numbers
		our_version = list(map(int, e['CCVERSION'].split('.')))
		if all([a >= b for a, b in zip(our_version, colour_version)]):
			e.AppendUnique(CCFLAGS = ['-fdiagnostics-color=always'])

	return env
