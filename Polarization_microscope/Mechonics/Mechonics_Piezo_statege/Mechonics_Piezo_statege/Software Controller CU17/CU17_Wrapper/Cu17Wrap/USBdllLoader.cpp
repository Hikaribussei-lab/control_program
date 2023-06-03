// ------------------------------------------ USB Dll Loader
#include <ctype.h>
#include <windows.h>
#include <math.h>      
#include <string.h>
#include <mbstring.h>
#include "DllLoader.h"
#include "USBdllLoader.h"




CU80USBdllLoader::CU80USBdllLoader()
{
  
	char szPathCu17    [MAX_PATH];
	char nameDll[] = "CU80USB1.dll"; 
	char nameD12[] = "Cu17Wrap.dll";
	char *pszdest  = NULL;
	char *pszPathCu17 = szPathCu17;
	DWORD nSizePath;
	HMODULE hModuleCu17wrap = NULL ;                             

	hModuleCu17wrap    = GetModuleHandle( nameD12 );
	if (hModuleCu17wrap)
	{
		nSizePath = GetModuleFileName( hModuleCu17wrap , szPathCu17 , MAX_PATH ) ;
		if (nSizePath)
		{
			pszdest = (char*) _mbsstr((unsigned char*) pszPathCu17, (unsigned char*) nameD12);
			if (pszdest)
			{
				ZeroMemory( pszdest , 2 ); 
				if (lstrcat(szPathCu17,nameDll))
				{
					LoadLibrary(szPathCu17);
				}
			}
		}
	}
    
  LoadLibrary(nameDll);

  // names of the functions are defined here
  strcpy_s(ifEcho                                  .Name,"Echo");
  strcpy_s(ifCU80Open			                     .Name,"CU80Open");
  strcpy_s(ifCU80Close                             .Name,"CU80Close");
  strcpy_s(ifCU80PiezoStop                         .Name,"CU80PiezoStop");
  strcpy_s(ifCU80DCDCon                            .Name,"CU80DCDCon");
  strcpy_s(ifCU80DCDCoff                           .Name,"CU80DCDCoff");
  strcpy_s(ifCU80PiezoMove                         .Name,"CU80PiezoMove");
  strcpy_s(ifGetUSBEEPromInfo			             .Name,"GetUSBEEPromInfo");  

  ifEcho										 .Status = ipsUnknown;
  ifCU80Open			                         .Status = ipsUnknown;
  ifCU80Close                                    .Status = ipsUnknown;
  ifCU80PiezoStop                                .Status = ipsUnknown;
  ifCU80DCDCon                                   .Status = ipsUnknown;
  ifCU80DCDCoff                                  .Status = ipsUnknown;
  ifCU80PiezoMove                                .Status = ipsUnknown;
  ifGetUSBEEPromInfo			                 .Status = ipsUnknown;
  
  ifEcho										 .ptrToFunc = NULL;
  ifCU80Open			                         .ptrToFunc = NULL;
  ifCU80Close                                    .ptrToFunc = NULL;
  ifCU80PiezoStop                                .ptrToFunc = NULL;
  ifCU80DCDCon                                   .ptrToFunc = NULL;
  ifCU80DCDCoff                                  .ptrToFunc = NULL;
  ifCU80PiezoMove                                .ptrToFunc = NULL;
  ifGetUSBEEPromInfo			                 .ptrToFunc = NULL;  
   
  Connect();
}

CU80USBdllLoader::~CU80USBdllLoader()
{

}
void CU80USBdllLoader::ConnectEntryPoint(ImportedFunc * ifPoint)
{
  ifPoint->ptrToFunc = GetProcAddress(ifPoint->Name,ifPoint->Status);      
}
void CU80USBdllLoader::Connect()
{   
   // An attempt is made to find all the pre-defined entry points in the dll
   
	ConnectEntryPoint(& ifEcho);									 
	ConnectEntryPoint(& ifCU80Open);			                         
	ConnectEntryPoint(& ifCU80Close);                                   
	ConnectEntryPoint(& ifCU80PiezoStop);                                
	ConnectEntryPoint(& ifCU80DCDCon);                                 
	ConnectEntryPoint(& ifCU80DCDCoff);                                 
	ConnectEntryPoint(& ifCU80PiezoMove);                                
	ConnectEntryPoint(& ifGetUSBEEPromInfo);
	
	

}
extern "C" void CallIt(DeviceRec * where, pCU80WOpen ptr);


bool CU80USBdllLoader::CU80Open(DeviceRec * pdevRec, char ** refStr)
{
  if ( IsLoaded() && (ifCU80Open.Status==ipsAvailable))
	{
		((pCU80WOpen)ifCU80Open.ptrToFunc)(&tempR, pdevRec);    
    * refStr = tempR.A;
    return true;      
	}
	else
		return false;
}
bool CU80USBdllLoader::CU80Close(DeviceRec devRec)
{
  if ( IsLoaded() && (ifCU80Close.Status==ipsAvailable))
	{
		
    ((pCU80WClose)ifCU80Close.ptrToFunc)(devRec);    
    return true;      
	}
	else
		return false;
}

bool CU80USBdllLoader::Echo(DeviceRec devRec, DWORD w, DWORD * result)
{
  if ( IsLoaded() && (ifEcho.Status==ipsAvailable))
	{
		
    *result = ((pCU80WEcho)ifEcho.ptrToFunc)(devRec,w);    
    return true;      
	}
	else
		return false;
}



bool CU80USBdllLoader::CU80PiezoStop(DeviceRec devRec)
{
  if ( IsLoaded() && (ifCU80PiezoStop.Status==ipsAvailable))
	{
		
    ((pCU80WPiezoStop)ifCU80PiezoStop.ptrToFunc)(devRec);    
    return true;      
	}
	else
		return false;
}




bool CU80USBdllLoader::CU80DCDCon(DeviceRec devRec)
{
  if ( IsLoaded() && (ifCU80DCDCon.Status==ipsAvailable))
	{
    ((pCU80WDCDCon)ifCU80DCDCon.ptrToFunc)(devRec);    
    return true;      
	}
	else
		return false;  
}

bool CU80USBdllLoader::CU80DCDCoff(DeviceRec devRec)
{
  if ( IsLoaded() && (ifCU80DCDCoff.Status==ipsAvailable))
	{
		
    ((pCU80WDCDCoff)ifCU80DCDCoff.ptrToFunc)(devRec); 
    return true;      
	}
	else
		return false;  
}

bool CU80USBdllLoader::CU80PiezoMove(DeviceRec devRec, INT32 axis, INT32 velocity ,INT32 voltage)
{
  if ( IsLoaded() && (ifCU80PiezoMove.Status==ipsAvailable))
	{
		
    ((pCU80WPiezoMove)ifCU80PiezoMove.ptrToFunc)(devRec, axis, velocity, voltage);    
    return true;      
	}
	else
		return false;  
}

bool CU80USBdllLoader::GetUSBEEPromInfo(DeviceRec devRec, USBEEProm * pResult)
{
  if ( IsLoaded() && (ifGetUSBEEPromInfo.Status==ipsAvailable))
	{		
    ((pCU80WGetEEPromInfo)ifGetUSBEEPromInfo.ptrToFunc)(pResult,devRec);    
    return true;      
	}
	else
		return false;  

}
