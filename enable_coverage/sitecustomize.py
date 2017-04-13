import os
import coverage

print('Enabling coverage measurement of this Python process...')

os.environ['COVERAGE_PROCESS_START'] = '.coveragerc'

coverage.process_startup()
