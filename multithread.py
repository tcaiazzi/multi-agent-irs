import threading
import subprocess





def programma1():
    try : 
        # Lancia RUN_RSP.py
        subprocess.run(["python3", '/home/matteo/Documenti/GitHub/tesiMagistrale/run_rsp.py'])

        # multithread ->
        #               lancia run_rsp->
        #                               che lancia rsp->
        #                                               che usa prePost
        #               alla fine lancia visualizza_reward_mosse


    except Exception as e :
        print(e)


t1 = threading.Thread(target=programma1)
#t2 = threading.Thread(target=programma2)

# Avviare i thread
t1.start()
#t2.start()

# Attendere che entrambi i thread terminino
#t1.join()
#t2.join()
