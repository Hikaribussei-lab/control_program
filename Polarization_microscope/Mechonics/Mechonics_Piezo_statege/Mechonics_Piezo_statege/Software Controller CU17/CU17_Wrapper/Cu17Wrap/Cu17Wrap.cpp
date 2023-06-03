// Cu17Wrap.cpp : Defines the entry point for the DLL application.
//

#include "stdafx.h"
#include "dllloader.h"
#include "usbdllloader.h"
#include "Cu17Wrap.h"

CU80USBdllLoader * usbDll = NULL;

BOOL APIENTRY DllMain( HANDLE hModule, 
                       DWORD  ul_reason_for_call, 
                       LPVOID lpReserved
					 )
{
    switch (ul_reason_for_call)
	{
		case DLL_PROCESS_ATTACH:
      CU80WrapperInit();
     break;
		case DLL_THREAD_ATTACH:
		case DLL_THREAD_DETACH:
    break;
		case DLL_PROCESS_DETACH:
        CU80WrapperDispose();
			break;
    }
    return TRUE;
}


DeviceRec ToDDR(DWORD USBInstance, DWORD USBVersion, DWORD DevID, DWORD EEID)
{
  DeviceRec ddr;
  ddr.DevID       = DevID;
  ddr.EEID        = EEID;
  ddr.USBInstance = USBInstance;
  ddr.USBVersion  = USBVersion;
  return ddr;
}
void FromDDR(DeviceRec ddr, DWORD* USBInstance, DWORD* USBVersion, DWORD* DevID, DWORD* EEID)
{
  *DevID = ddr.DevID;
  *EEID = ddr.EEID;
  *USBInstance = ddr.USBInstance;
  *USBVersion = ddr.USBVersion;
}


extern "C" CU80WRAP_API void __stdcall CU80WrapperInit()
{
  if(usbDll ==  NULL)
    usbDll = new CU80USBdllLoader();
}
extern "C" CU80WRAP_API void __stdcall CU80WrapperDispose()
{
  if(usbDll != NULL)
  {
    delete usbDll;
    usbDll = NULL;
  }
}
// function  GetUSBEEPromInfo(MUSBDeviceID:DeviceRec): USBEEProm; stdcall

extern "C" CU80WRAP_API DWORD __stdcall CU80WEcho(DWORD USBInstance, DWORD USBVersion, DWORD DevID, DWORD EEID, DWORD w)
{
  if(!usbDll)
    return -1; // error
  
  DeviceRec devRec = ToDDR(USBInstance, USBVersion, DevID, EEID);
  DWORD res = 0;
  bool bSuccess = usbDll->Echo(devRec,w,&res); 
  return res;
}
extern "C" CU80WRAP_API char * __stdcall CU80WOpen(DWORD* USBInstance, DWORD* USBVersion, DWORD* DevID, DWORD* EEID)
{
  static char * refStr;
  static DeviceRec ddr;

  if(!usbDll)
    return NULL;
  refStr = NULL;
  ddr = ToDDR(*USBInstance, *USBVersion, *DevID, *EEID);
  usbDll->CU80Open(&ddr,&refStr); 
  FromDDR(ddr, USBInstance, USBVersion, DevID, EEID);
  return refStr;       
}
extern "C" CU80WRAP_API void __stdcall CU80WClose(DWORD USBInstance, DWORD USBVersion, DWORD DevID, DWORD EEID)
{
  DeviceRec ddr;
  if(!usbDll)
    return;
  ddr = ToDDR(USBInstance, USBVersion, DevID, EEID);
  usbDll->CU80Close(ddr); 
}
extern "C" CU80WRAP_API void __stdcall CU80WPiezoStop(DWORD USBInstance, DWORD USBVersion, DWORD DevID, DWORD EEID)
{
  DeviceRec ddr;
  if(!usbDll)
    return;
  ddr = ToDDR(USBInstance, USBVersion, DevID, EEID);
  usbDll->CU80PiezoStop(ddr); 
}



extern "C" CU80WRAP_API void __stdcall CU80WDCDCon(DWORD USBInstance, DWORD USBVersion, DWORD DevID, DWORD EEID)
{
  DeviceRec ddr;
  if(!usbDll)
    return;
  ddr = ToDDR(USBInstance, USBVersion, DevID, EEID);
  usbDll->CU80DCDCon(ddr); 
}
extern "C" CU80WRAP_API void __stdcall CU80WDCDCoff(DWORD USBInstance, DWORD USBVersion, DWORD DevID, DWORD EEID)
{
  DeviceRec ddr;
  if(!usbDll)
    return;
  ddr = ToDDR(USBInstance, USBVersion, DevID, EEID);
  usbDll->CU80DCDCoff(ddr); 
}



extern "C" CU80WRAP_API void __stdcall CU80WPiezoMove(DWORD USBInstance, DWORD USBVersion, DWORD DevID, DWORD EEID, INT32 Axis, INT32 Velocity, INT32 Voltage)
{
  DeviceRec ddr;
  if(!usbDll)
    return;
  ddr = ToDDR(USBInstance, USBVersion, DevID, EEID);
  usbDll->CU80PiezoMove(ddr, Axis, Velocity, Voltage);
}

extern "C" CU80WRAP_API void __stdcall CU80WGetEEPROMInfo(
                                            DWORD USBInstance, DWORD USBVersion, DWORD DevID, DWORD EEID,  
                                            DWORD* USBVendorID,
                                            DWORD* USBProductID,
                                            DWORD* USBDeviceID,
                                            DWORD* DeviceID,
                                            DWORD* EEPromID,
                                            DWORD* Version,
                                            DWORD* SerialNumber,
                                            DWORD* CustomerID,
                                            char*  Company, //[32]
                                            char*  Date,    //[32]
                                            char*  ProductStr,//[32]
                                            char*  Customer,//[32]
                                            char*  CustomerStr)//[32]
{
  DeviceRec ddr;
  if(!usbDll)
    return;
  ddr = ToDDR(USBInstance, USBVersion, DevID, EEID);
  USBEEProm usbep;
  bool res = usbDll->GetUSBEEPromInfo (ddr,&usbep);
  if(!res) return;
  *USBVendorID  = usbep.USBVendorID;
  *USBProductID = usbep.USBProductID;
  *USBDeviceID  = usbep.USBDeviceID; 
  *DeviceID     = usbep.DeviceID;
  *EEPromID     = usbep.EEPromID;
  *Version      = usbep.Version;
  *SerialNumber = usbep.SerialNumber;
  *CustomerID   = usbep.CustomerID;
  memcpy(Company,usbep.Company,32);
  memcpy(Date,usbep.Date,32);
  memcpy(ProductStr,usbep.ProductStr,32);
  memcpy(Customer,usbep.Customer,32);
  memcpy(CustomerStr, usbep.CustomerStr,32);   
}