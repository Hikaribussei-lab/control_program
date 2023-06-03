// typedef section contains the actual functions definitions
typedef struct r256
{
  char A[256];
} R256;
typedef struct r32
{
  char A[32];
} R32;
typedef struct r16
{
  char A[32];
} R16;

typedef struct delphiDevRec
{
  DWORD USBInstance;
  DWORD USBVersion;
  DWORD DevID;
  DWORD EEID;
} DeviceRec;
typedef struct delphiIEE
{
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
} USBEEProm;

typedef  DWORD (__stdcall*  pCU80WEcho)(DeviceRec devRec, DWORD w);
typedef  void  (__stdcall*  pCU80WOpen)(R256 * result, DeviceRec * pdevRec);
typedef  void  (__stdcall*  pCU80WClose)(DeviceRec devRec); 
typedef  void  (__stdcall*  pCU80WPiezoStop)(DeviceRec devRec);
typedef  void  (__stdcall*  pCU80WDCDCon)(DeviceRec devRec); 
typedef  void  (__stdcall*  pCU80WDCDCoff)(DeviceRec devRec);
typedef  void  (__stdcall*  pCU80WPiezoMove)(DeviceRec devRec, INT32 Axis, INT32 Velocity, INT32 Voltage);
typedef  void  (__stdcall*  pCU80WGetEEPromInfo)(USBEEProm * usbe, DeviceRec devRec);
class CU80USBdllLoader : public DllLoader
{
  public:
    CU80USBdllLoader();
    ~CU80USBdllLoader();
    void Connect();
  private:
    // Function status structures
    
	ImportedFunc ifEcho;									 
	ImportedFunc ifCU80Open;			                         
	ImportedFunc ifCU80Close;                                   
	ImportedFunc ifCU80PiezoStop;                                
	ImportedFunc ifCU80DCDCon;                                 
	ImportedFunc ifCU80DCDCoff;                                 
	ImportedFunc ifCU80PiezoMove;                                
	ImportedFunc ifGetUSBEEPromInfo;			                     
    
	R256 tempR;
  protected:
    void ConnectEntryPoint(ImportedFunc * ifPoint);
  public: 
    // function prototypes
    bool Echo(DeviceRec devRec, DWORD w, DWORD * result);
    bool CU80Open(DeviceRec * pdevRec, char ** refStr);
    bool CU80Close(DeviceRec devRec); 
    bool CU80DCDCon (DeviceRec devRec); 
    bool CU80DCDCoff(DeviceRec devRec);
    bool CU80PiezoStop(DeviceRec devRec);
    bool CU80PiezoMove(DeviceRec devRec, INT32 axis, INT32 velocity ,INT32 voltage);
    bool GetUSBEEPromInfo(DeviceRec devRec, USBEEProm * pResult);
};

