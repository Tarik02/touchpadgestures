import os
from setuptools import setup


def read(fname: str):
	return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
	name='touchpadgestures',
	version='0.1.0',
	author='Tarik02',
	description='Recognize touchpad gestures using synclient -ms',
	long_description=read('README.md'),
	long_description_content_type='text/markdown',
	license='MIT',
	keywords='Linux X11 TouchPad',
	url='https://github.com/Tarik02/touchpadgestures',
	packages=['touchpadgestures'],
	python_requires='>=3.7.0',
	classifiers=[
		'Development Status :: 3 - Alpha',
		'License :: OSI Approved :: MIT License',
		'Operating System :: Linux',
		'Programming Language :: Python :: 3.7',
		'Topic :: Utilities',
		'Typing :: Typed',
	],
	include_package_data=True,
	entry_points={
		'console_scripts': [
			'touchpadgestures = touchpadgestures:main',
		],
	},
	project_urls={
		'Issues': 'https://github.com/Tarik02/touchpadgestures/issues',
		'Pull Requests': 'https://github.com/Tarik02/touchpadgestures/pulls',
		'Source': 'https://github.com/Tarik02/touchpadgestures',
	},
)
