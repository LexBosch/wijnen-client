
from distutils.core import setup
setup(
  name = 'wijnen',       
  packages = ['wijnen'],  
  version = '0.2',
  license='MIT',       
  description = 'Client to connect to the wijnen web-api',  
  author = 'Lex Bosch',                  
  author_email = 'lexbosch@live.nl',     
  url = 'https://github.com/LexBosch/wijnen-client', 
  download_url = 'https://github.com/LexBosch/wijnen-client/archive/0.2.tar.gz',
  keywords = ['wijnen', 'api', 'client'],   
  install_requires=[            
          'requests',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',    
    'Intended Audience :: Developers',      
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',  
    'Programming Language :: Python :: 3',     
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',


],
)
