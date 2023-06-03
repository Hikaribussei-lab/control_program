// Cu17App.cpp : Defines the entry point for the console application.

#include "stdio.h"
#include "stdafx.h"
#include "Cu17Wrap.h"

					 
int _tmain(int argc, _TCHAR* argv[])
{
  CU80WrapperInit();
  DWORD USBInstance = 0;
  DWORD USBVersion  = 1;
  DWORD DevID       = 2;
  DWORD EEID        = 0;
  DWORD USBVendorID;
  DWORD USBProductID;
  DWORD USBDeviceID;
  DWORD DeviceID;
  DWORD EEPromID;
  DWORD Version;
  DWORD SerialNumber;
  DWORD CustomerID;
  char  Company[32];
  char  Date[32];
  char  ProductStr[32];
  char  Customer[32];
  char  CustomerStr[32];
  int   i,axis,iter,vel,volt,time;
  DWORD Echo;

  char*  buff = CU80WOpen(&USBInstance, &USBVersion, &DevID, &EEID);;
  printf ("\nCU80WOpen()");
  printf ("\nError Message (empty if no error): %s",buff);
  
  if(strlen(buff)== 0)
  {
	CU80WDCDCon (USBInstance, USBVersion, DevID, EEID);
	printf("\n\nCU80DCDCon()");
	Echo = 42;
	Echo = CU80WEcho(USBInstance, USBVersion, DevID, EEID, Echo);
	CU80WGetEEPROMInfo(USBInstance, USBVersion, DevID, EEID,
		& USBVendorID,
		& USBProductID,
		& USBDeviceID,
		& DeviceID,
		& EEPromID,
		& Version,
		& SerialNumber,
		& CustomerID,
		Company,
		Date,
		ProductStr,
		Customer,
		CustomerStr);       

	printf("\n\nCU80WGetEEPROMInfo()");
	printf("\nUSBVendorID: %d \nUSBProductID: %d \nUSBDeviceID: %d",USBVendorID,USBProductID,USBDeviceID);
	printf("\nDeviceID: %d \nEEPromID: %d \nVersion: %d"           ,DeviceID   ,EEPromID    ,Version);
	printf("\nCustomerID: %d \nCompany: %s \nDate: %s"             ,CustomerID ,Company     ,Date);
	printf("\nProductStr: %s \nCustomer: %s \nCustomerStr: %s"     ,ProductStr ,Customer    ,CustomerStr);

	CU80WPiezoStop(USBInstance, USBVersion, DevID, EEID);
	
	printf("\n\n(1 - X Axis,2 - Y Axis,3 - Z Axis)");
	printf("\nInput Axis:");
	scanf_s("%d",&axis);
	printf("\n\nVelocity:\n(0 - stop and set voltage),\
		   \n[-1,+1] single step and set voltage,\
		   \n[-63...-2,2...63] move and set voltage");
	printf("\n\nInput Velocity:");
	scanf_s("%d",&vel);
	printf("\n\nVoltage [22..40]:");
	printf("\nInput Voltage:");
	scanf_s("%d",&volt);	
	printf("\n\nIterations [0 .. 10]:");
	printf("\nInput iterations:");
	scanf_s("%d",&iter);
	printf("\n\nInput sleep time between steps:");
	printf("\ntime [50 .. 150]ms:");
	scanf_s("%d",&time);
	while(getchar()!='\n');
	if (axis  < 1 ) axis = 1;
	if (axis  > 3 ) axis = 3;
	if (vel   < -63) vel = -63;
	if (vel   > 63) vel = 63;
	if (volt  < 22 ) volt = 22;
	if (volt  > 40 ) volt = 40; // if (volt  > 82 ) volt = 82;
	if (iter < 0 ) iter = 0; 
	if (iter > 10) iter = 10;
	if (time  < 50) time = 50;
	if (time  > 150) time = 150;
	iter++;	
	do
	{			
		for( i = 0; i < iter;i++)
		{
		CU80WPiezoMove(USBInstance, USBVersion, DevID, EEID, 
			axis,		// Axis
			vel,		// Velocity   
			volt);		// Voltage
		Sleep(time);
		}				
		CU80WPiezoStop(USBInstance, USBVersion, DevID, EEID);
		printf("\nInput (s - stop, r - repeat):");
	}while(getchar()!='s');
	CU80WDCDCoff (USBInstance, USBVersion, DevID, EEID);
	CU80WClose(USBInstance, USBVersion, DevID, EEID);
    printf("\n\nCU80WClose()");
  }
  CU80WrapperDispose();	
  printf("\n\nCU80WrapperDispose()");
  printf("\n\nPress return to continue");
  while(getchar()!='\n');
  getchar();
  return 0;
}