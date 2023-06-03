#include <ctype.h>
#include <windows.h>
#include <math.h>      
#include <string.h>

#include "DllLoader.h"

DllLoader::DllLoader()
{
  m_pszModule = NULL;
}
DllLoader::~DllLoader()
{
	if( m_bManaged && m_module )
		::FreeLibrary(m_module);
	m_module  = NULL;
	m_bManaged = FALSE;
	if( m_pszModule )
		delete m_pszModule;
	m_pszModule = NULL;
}

BOOL DllLoader::LoadLibraryName(LPCTSTR pszLibrary)
{
	if( !m_pszModule )
	{
		if( pszLibrary && *pszLibrary)
		{
			int nLen = lstrlen(pszLibrary); 
			m_pszModule = new TCHAR[nLen+2]; 
			if( m_pszModule ) 
			{ 
				ZeroMemory( m_pszModule, sizeof(TCHAR)*(nLen+2) ); 
				lstrcpy(m_pszModule,pszLibrary); 
			} 
			else 
			{ 
				// ASSERT(!"DllLoader::dll_LoadLibrary - Unable to allocate memory for a string!"); 
			}
      return TRUE;
		}
    else
      return FALSE; 
  }
  else
  {
    // we should change the name
    delete m_pszModule;
	  m_pszModule = NULL;
    return LoadLibraryName(pszLibrary);
  }
}
BOOL DllLoader::LoadLibrary(LPCTSTR pszLibrary)
{
	if(!LoadLibraryName(pszLibrary))
    return FALSE;
	
  // Load the DLL
	m_dwLoadLibError = 0;
	m_module = ::LoadLibrary(pszLibrary);
	if( m_module )
		return TRUE;

	// Unable to load it, find out why
	m_dwLoadLibError = GetLastError();

	if( !m_dwLoadLibError )
	{
		m_dwLoadLibError = 0x20000000;
	}

	return FALSE;
}

FARPROC DllLoader::GetProcAddress(LPCSTR pszFunctionName, ImportedProcState& ips)
{
	FARPROC pfn = NULL;
	ips = ipsUnknown;
	
	// Does the DLL still need to be loaded?
	if( !m_module && m_pszModule && *m_pszModule && 
		  0 == m_dwLoadLibError   // There is no reason to attempt to load the DLL more than once
		)
	{
		LoadLibrary(m_pszModule);
	}

	if( m_module )
	{		
		pfn = ::GetProcAddress(m_module,pszFunctionName);
		if( pfn )
			ips = ipsAvailable;
		else
			ips = ipsMissing;
	}

	return pfn; 
}




DWORD DllLoader::GetLoadError()  
{
	return m_dwLoadLibError;     
}


BOOL DllLoader::IsLoaded()      
{ 
	return NULL!=m_module;       
}


LPCTSTR DllLoader::GetModuleName() 
{ 
	return (LPCTSTR)m_pszModule; 
}

