import math
def findIQR(arr):
    arr.sort()
    lenn=len(arr)
    leen=(lenn//2)//2
    if(lenn%2==1):
        if((lenn//2)%2==1):
            midR=arr[leen]
            midL=arr[-(leen+1)]
        
        else:
            midR=( arr[leen] + arr[leen-1] ) / 2
            midL=( arr[-leen] + arr[-(leen+1)] ) / 2
        
    
    else:
        if((lenn//2)%2==1):
            midR=arr[leen]
            midL=arr[-(leen+1)]
        
        else:
            midR=( arr[leen] + arr[leen-1] ) / 2
            midL=( arr[-leen] + arr[-(leen+1)] ) / 2
        
    iqr=midL-midR
    return (iqr,midL,midR)
def checkOutlier(arr):
    #find AVG
    avg=0
    for i in range(len(arr)):
        avg+=arr[i]
    avg=avg/len(arr)
    # find Variance
    variance=0
    for i in range(len(arr)):
        variance+=math.pow((arr[i]-avg),2)
    variance=variance/(len(arr)-1)

    stdv=math.sqrt(variance)

    # tim gia tri bien lon nhat(phia ngon), be nhat (phia goc)
    uw=avg+stdv*3
    lw=avg-stdv*3
    uw=round(uw,2)
    lw=round(lw,2)
    return (uw,lw)

def checkOutlierV2(arr):
    try:
        (iqr,q3,q1)=findIQR(arr)
        lower_limit=q1-(iqr*1.5)
        upper_limit=q3+(iqr*1.5)
        lower_limit=round(lower_limit,2)
        upper_limit=round(upper_limit,2)
        return(upper_limit,lower_limit)
    except:
        return (35,37.5)
