#include "DigitalSearch.h"
#pragma comment(linker,"\"/manifestdependency:type='win32' \
name='Microsoft.Windows.Common-Controls' version='6.0.0.0' \
processorArchitecture='*' publicKeyToken='6595b64144ccf1df' language='*'\"")

#pragma warning(disable: 6386)

BOOL
InsertString(
	DIGITAL_TREE dt,
	PCTSTR str,
	PBOOL uniq)
{
	if (!(dt && str && uniq))
		return EXIT_FAILURE;

	INT len = lstrlen(str);
	PINT arr = malloc(len * sizeof(INT));
	if (!arr)
		return EXIT_FAILURE;

	for (INT i = 0; i < len; ++i)
		arr[i] = str[i];

	BOOL r = DTInsert(dt, arr, len, uniq);
	free(arr);
	return r;
}

#pragma warning(disable: 4711)

BOOL
FindString(
	DIGITAL_TREE dt,
	PCTSTR str,
	PBOOL res)
{
	if (!(dt && str && res))
		return EXIT_FAILURE;

	INT len = lstrlen(str);
	PINT arr = malloc(len * sizeof(INT));
	if (!arr)
		return EXIT_FAILURE;

	for (INT i = 0; i < len; ++i)
		arr[i] = str[i];

	BOOL r = DTFind(dt, arr, len, res);
	free(arr);
	return r;
}

#pragma warning(default: 6386)

#define BTN_0 1000
#define BTN_1 1001
#define USR_BUFF_SIZE 32
#define DISPLAY_BUFF_SIZE 128

LRESULT
WndProc(
	HWND hWnd,
	UINT message,
	WPARAM wParam,
	LPARAM lParam)
{
	static HWND edits[4];
	static DIGITAL_TREE dt;
	static TCHAR str[USR_BUFF_SIZE];
	static TCHAR buff[DISPLAY_BUFF_SIZE];
	static BOOL unique;
	static BOOL res;

	switch (message)
	{
		case WM_CREATE:
		{
			dt = DTCreate();

			edits[0] = CreateWindow(_T("edit"), NULL, WS_CHILD | WS_VISIBLE | WS_BORDER | ES_CENTER, 10, 10, 200, 30, hWnd, NULL, NULL, NULL);
			edits[1] = CreateWindow(_T("edit"), NULL, WS_CHILD | WS_VISIBLE | WS_BORDER | ES_CENTER, 10, 50, 200, 30, hWnd, NULL, NULL, NULL);
			edits[2] = CreateWindow(_T("edit"), NULL, WS_CHILD | WS_VISIBLE | WS_BORDER | ES_CENTER | ES_READONLY, 10, 90, 280, 20, hWnd, NULL, NULL, NULL);
			edits[3] = CreateWindow(_T("edit"), NULL, WS_CHILD | WS_VISIBLE | WS_BORDER | ES_CENTER | ES_READONLY | ES_MULTILINE, 10, 120, 280, 100, hWnd, NULL, NULL, NULL);

			CreateWindow(_T("button"), _T("Insert"), WS_CHILD | WS_VISIBLE, 220, 10, 70, 30, hWnd, (HMENU)BTN_0, NULL, NULL);
			CreateWindow(_T("button"), _T("Find"), WS_CHILD | WS_VISIBLE, 220, 50, 70, 30, hWnd, (HMENU)BTN_1, NULL, NULL);

			break;
		}

		case WM_COMMAND:
		{
			switch (LOWORD(wParam))
			{
				case BTN_0:
				{
					if (!GetWindowText(edits[0], str, USR_BUFF_SIZE))
					{
						SetWindowText(edits[2], _T("Empty line"));
						break;
					}
					
					if (InsertString(dt, str, &unique))
					{
						SetWindowText(edits[2], _T("System error"));
						break;
					}

					if (unique)
					{
						GetWindowText(edits[3], buff, DISPLAY_BUFF_SIZE);
						_tcscat_s(buff, DISPLAY_BUFF_SIZE, str);
						_tcscat_s(buff, DISPLAY_BUFF_SIZE, _T("\r\n"));
						SetWindowText(edits[3], buff);
						SetWindowText(edits[0], NULL);
						SetWindowText(edits[2], _T("Success"));
					}
					else
						SetWindowText(edits[2], _T("Duplication"));

					break;
				}

				case BTN_1:
				{
					if (!GetWindowText(edits[1], str, USR_BUFF_SIZE))
					{
						SetWindowText(edits[2], _T("Empty line"));
						break;
					}
					
					if (FindString(dt, str, &res))
					{
						SetWindowText(edits[2], _T("System error"));
						break;
					}

					SetWindowText(edits[2], res ? _T("Data found") : _T("Data not found"));

					break;
				}
			}
			break;
		}

		case WM_DESTROY:
		{
			PostQuitMessage(EXIT_SUCCESS);
			break;
		}

		default:
			return DefWindowProc(hWnd, message, wParam, lParam);
	}

	return EXIT_SUCCESS;
}

#pragma warning(default: 4711)

INT
_tWinMain(
	_In_ HINSTANCE hInstance,
	_In_opt_ HINSTANCE hPrevInstance,
	_In_ LPWSTR lpCmdLine,
	_In_ INT nCmdShow)
{
	UNREFERENCED_PARAMETER(hPrevInstance);
	UNREFERENCED_PARAMETER(lpCmdLine);

	WNDCLASS wc = { 0 };
	wc.lpfnWndProc = WndProc;
	wc.hbrBackground = (HBRUSH)(COLOR_WINDOW + 1);
	wc.lpszClassName = _T("MainWindow");

	if (!RegisterClass(&wc))
		return EXIT_FAILURE;

	HWND hWnd = CreateWindow(
		wc.lpszClassName,
		NULL, WS_OVERLAPPEDWINDOW,
		700, 300, 315, 270,
		NULL, NULL, hInstance, NULL);

	if (!hWnd)
		return EXIT_FAILURE;

	ShowWindow(hWnd, nCmdShow);
	UpdateWindow(hWnd);

	MSG msg;
	while (GetMessage(&msg, NULL, 0, 0))
	{
		TranslateMessage(&msg);
		DispatchMessage(&msg);
	}

	return (INT)msg.wParam;
}