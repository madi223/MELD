#!/usr/bin/env python3

from asynciojobs import Scheduler
from apssh import SshNode, ColonFormatter
from apssh import SshJob, Run, RunScript, Pull
import argparse
######## ARGS definition ######                                                                                                                                                               
parser = argparse.ArgumentParser()
parser.add_argument("--slice","-s",help="Slice name",required=True)
args = parser.parse_args()
##############################                                                                                                                                                                
gwname = "faraday.inria.fr"
slice = args.slice

def main(epc,enb,server,ue,awgn, *, verbose=True):

    # show ssh outputs on stdout as they appear
    # together with corresponding hostname
    formatter = ColonFormatter(verbose=verbose)
    
    ########## declare the needed ssh connections
    # our main ssh connection
    gateway = SshNode(hostname = gwname, username = slice,
                      formatter = formatter)
    
    ########## 
    job_warmup = SshJob(
        node = gateway,
        # with just Run()
        # you can run a command already available on the remote
        command = [
            Run("rhubarbe load -i flex-epc", epc),
            Run("rhubarbe load -i flex-enb", enb),
            Run("rhubarbe load -i flex-pico-ue", ue),
            Run("rhubarbe load -i flex-pico-server", server),
            Run("rhubarbe load -i u16.48-gnuradio-3.7.10-uhd-images", awgn),
            Run("rhubarbe wait", enb, ue, awgn,epc,server),
            Run("rhubarbe on", enb, ue, awgn),
            Run("uon", enb, ue, awgn),
        ]
    )
   
    epc,enb,ue,server,awgn = [
    SshNode(hostname = nodename, username="root",
                # this is how we create a 2-hop                                                                                                                                               
                # ssh connection behind a gateway                                                                                                                                             
            gateway = gateway,
            formatter = formatter, debug=verbose)
    for nodename in (epc,enb,ue,server,awgn)]

    job_server = SshJob(
        node = server,
        command = RunScript("server_config.sh"),
        required = job_warmup,
    )

    job_noise = SshJob(
        node = awgn,
        command = RunScript("noise_config.sh"),
        required = job_warmup,
    )

    job_epc = SshJob(
        node = epc
        command = RunScript("epc_config.sh"),
        required = job_noise,
    )
        
    scheduler = Scheduler(
        job_warmup,
        job_server,
        job_noise,
        job_epc,
        verbose=verbose
    )

    scheduler.export_as_dotfile('demo.dot')
    print("# produce .png file with the following command")
    print("# install dot with e.g. brew install graphviz on macos")
    print("dot -Tpng demo.dot -o demo.png")
    print(20 * '=')

    ok = scheduler.orchestrate()
    if not ok:
        scheduler.debrief()

if __name__ == '__main__':
    main('fit17', 'fit23','fit14','fit06','fit13', verbose=False)
