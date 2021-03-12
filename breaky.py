import requests

def main():

    iptarg="105.211.134.155"
    location = getloc(iptarg)
    print("You in %s" % location)

main()
