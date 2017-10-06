# USAGE:
# python test-suite.py path/to/your/script

import imp
import argparse
import signal

def main(script_path):
    print "importing!"
    new_module = imp.load_source('main', script_path)
    new_module = reload(new_module)
    print "imported!"
    signal.alarm(2)
    print "beginning tests"

    try:
        a = new_module.main(0,[],[])
        a = new_module.main(1,[1],[0])
        a = new_module.main(5,[0,0,0,0,0,0],[1,0,1,0,1,0])
    
    except TimeoutException:
        print 'Error code T'
        print 'Signal timed out'
        raise AssertionError
    
    finally:
        signal.alarm(0)
    
    if a!=True and a!=False and a!=1 and a!=0:
        print 'Error code 2'
        print 'Function returned unexpected value'
        raise AssertionError
    print "tests passed"

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('path', type=str)
    args = parser.parse_args()
    main(args.path)
