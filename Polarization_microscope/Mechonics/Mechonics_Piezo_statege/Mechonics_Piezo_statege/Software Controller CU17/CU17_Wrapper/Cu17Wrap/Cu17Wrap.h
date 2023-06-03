
// The following ifdef block is the standard way of creating macros which make exporting 
// from a DLL simpler. All files within this DLL are compiled with the CU80WRAP_EXPORTS
// symbol defined on the command line. This symbol should not be defined on any project
// that uses this DLL. This way any other project whose source files include this file see 
// CU80WRAP_API functions as being imported from a DLL, where this DLL sees symbols
// defined with this macro as being exported.
#ifdef CU80WRAP_EXPORTS
#define CU80WRAP_API __declspec(dllexport)
#else
#define CU80WRAP_API __declspec(dllimport)
#endif

// Function definitions. Note, that if it is neccessary to change the calling convention
// (to __cdecl for example), the according changes must be done also in CU17Wrap.cpp


extern "C" CU80WRAP_API DWORD __stdcall  CU80WEcho(DWORD  USBInstance, DWORD USBVersion, DWORD DevID, DWORD EEID, DWORD w);
extern "C" CU80WRAP_API char * __stdcall CU80WOpen(DWORD* USBInstance, DWORD* USBVersion, DWORD* DevID, DWORD* EEID);
extern "C" CU80WRAP_API void __stdcall   CU80WClose(DWORD USBInstance, DWORD USBVersion, DWORD DevID, DWORD EEID); 
extern "C" CU80WRAP_API void __stdcall   CU80WPiezoStop(DWORD USBInstance, DWORD USBVersion, DWORD DevID, DWORD EEID);
extern "C" CU80WRAP_API void __stdcall   CU80WDCDCon(DWORD USBInstance, DWORD USBVersion, DWORD DevID, DWORD EEID); 
extern "C" CU80WRAP_API void __stdcall   CU80WDCDCoff(DWORD USBInstance, DWORD USBVersion, DWORD DevID, DWORD EEID);
extern "C" CU80WRAP_API void __stdcall   CU80WPiezoMove(DWORD USBInstance, DWORD USBVersion, DWORD DevID, DWORD EEID, INT32 Axis, INT32 Velocity, INT32 Voltage);
extern "C" CU80WRAP_API void __stdcall   CU80WGetEEPROMInfo(
                                            DWORD  USBInstance, DWORD USBVersion, DWORD DevID, DWORD EEID,
                                            DWORD* USBVendorID,
                                            DWORD* USBProductID,
                                            DWORD* USBDeviceID,
                                            DWORD* DeviceID,
                                            DWORD* EEPromID,
                                            DWORD* Version,
                                            DWORD* SerialNumber,
                                            DWORD* CustomerID,
                                            char*  Company,		//[32]
                                            char*  Date,		//[32]
                                            char*  ProductStr,	//[32]
                                            char*  Customer,	//[32]
                                            char*  CustomerStr);//[32]

extern "C" CU80WRAP_API void __stdcall CU80WrapperInit();
extern "C" CU80WRAP_API void __stdcall CU80WrapperDispose();
