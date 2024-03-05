import os, sys, time

def main(props):
    print(props)

# ------------------------------------------

if __name__ == '__main__':
    props = {} 
    props['prop'] = 'xxx'

    start = time.time()
    main(props)
    print('DONE in:', time.strftime("%H:%M:%S", time.gmtime(time.time() - start)))

