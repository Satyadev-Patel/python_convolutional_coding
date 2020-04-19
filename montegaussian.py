import random
import math
snr=[0,0.5,1,1.5,2,2.5,3,3.5,4,4.5,5,5.5,6,6.5,7,7.5,8]
pb=[0.01587,0.01447,0.01309,0.01173,0.01040,0.00912,0.00789,0.00673,0.00565,0.00466,0.00377,0.00298,0.00230,0.00173,0.00126,0.00089,0.00060]
#print(pb)
ber=[0]*2000
ans=[0]*17
for q in range(0,17):
    k=500
    cnt=0
    for u in range(0,20000):
        x=[None]*k
        for i in range(0,k):
            x[i]=random.choice([0,1])
        m=[None]*(k+4)
        for i in range(0,k):
            x[i]=int(x[i])
        code=x
        for i in range(0,len(x)+4):
            if i<2 or i>=len(x)+2:
                m[i]=0
            else:
                m[i]=x[i-2]
        count=0
        e=[None]*(2*k+4)
        for i in range(2,len(m)):
            parity_1=(m[i]+m[i-2]+m[i-1])%2
            parity_2=(m[i]+m[i-2])%2
            e[count]=parity_1
            e[count+1]=parity_2
            count=count+2
        #gaussian starts here
        snr1=snr[q]/10
        snr_linear=10**snr1
        variance_square=1/snr_linear
        variance=math.sqrt(variance_square)/2.45
        f_term=1/(math.sqrt(2*3.14)*variance)
        for i in range(0,len(e)):
            e[i]=2*e[i]-1
        ran_nums=[i/10000 for i in range(1900,4000,1)]
        for i in range(0,len(e)):
            e[i]=float(e[i])
        for i in range(0,len(e)):
            x1=random.choice(ran_nums)
            x2=random.choice(ran_nums)
            if x1>x2:
                value=math.sqrt(-2*variance*math.log((x1)/f_term))
            else:
                value=math.sqrt(-2*variance*math.log(x2/f_term))
            sign_chk=random.choice([0,1])
            if sign_chk==0:
                value=-value
            e[i]=e[i]+value
        for i in range(0,len(e)):
            if e[i]<0:
                e[i]=0
            else:
                e[i]=1
        #gaussian ends here
        st=[0,0,1,1,1,0,0,1]
        st1=[1,1,0,0,0,1,1,0]
        n=k+2
        a=e
        b = [ [ None for i in range(4) ] for j in range(n) ]
        decoded=[None for i in range(n)]
        b[0][2]=1000
        b[0][3]=1000
        for j in range(0,2):
            b[0][j]=0;
            if st[j*2]!=a[0*2]:
                b[0][j]+=1
            if st[j*2+1]!=a[0*2+1]:
                b[0][j]+=1
        for i in range(1,n):
            for j in range(0,4):
                if j<2:
                    x=b[i-1][0];
                    if st[j*2]!=a[i*2]:
                        x+=1
                    if st[j*2+1]!=a[i*2+1]:
                        x+=1
                    y=b[i-1][2];
                    if st1[j*2]!=a[i*2]:
                        y+=1
                    if st1[j*2+1]!=a[i*2+1]:
                        y+=1

                    if x<y:
                        b[i][j]=x
                    if x>=y:
                        b[i][j]=y
                
                
                else:
                    x=b[i-1][1]
                    if st[j*2]!=a[i*2]:
                        x+=1
                    if st[j*2+1]!=a[i*2+1]:
                        x+=1


                    y=b[i-1][3] 
                    if st1[j*2]!=a[i*2]:
                        y+=1
                    if st1[j*2+1]!=a[i*2+1]:
                        y+=1
    
                    
                    if x<=y:
                        b[i][j]=x
                    if x>y:
                        b[i][j]=y
        x=0
        y=x
        for i in range(0,n):
            if x==0 or x==2:
                if b[i][0]>b[i][1]:
                    x=1
                if b[i][0]<b[i][1]:
                    x=0
                if b[i][0]==b[i][1]:
                    if i+1==n:
                        x=1
                    else:
                        if b[i+1][0]>b[i+1][1]:
                            a1=b[i+1][1]
                        else:
                            a1=b[i+1][0]

                        if b[i+1][2]>b[i+1][3]:
                            b1=b[i+1][3];
                        else:
                            b1=b[i+1][2];
    
                        if a1>b1:
                            x=1
                        elif b1>=a1:
                            x=0



            if x==1 or x==3:    
                if b[i][2]>b[i][3]:
                    x=3
                if b[i][2]<b[i][3]:
                    x=2
                if b[i][2]==b[i][3]:
                    if i+1==n:
                        x=2
                    else:
                        if b[i+1][0]>b[i+1][1]:
                            a1=b[i+1][1]
                        else:
                            a1=b[i+1][0]
    
                        if b[i+1][2]>b[i+1][3]:
                            b1=b[i+1][3]
                        else:
                            b1=b[i+1][2]

                        if a1>b1:
                            x=3
                        elif b1>=a1:
                            x=2



            decoded[i]=x%2
        count=0
       # print(code)
        #print(decoded)
        for i in range(0,len(code)):
            if code[i]!=decoded[i]:
                count=count+1
        cnt=cnt+count
    print("SNR:{}  Error Bits:{}".format(snr[q],cnt))
    ans[q]=cnt/(20000*k)
print("BER:{}".format(ans))
print("!")
