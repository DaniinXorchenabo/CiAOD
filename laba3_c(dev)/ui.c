#include <windows.h>
#include <tchar.h>

#pragma comment(linker,"\"/manifestdependency:type='win32' \
name='Microsoft.Windows.Common-Controls' version='6.0.0.0' \
processorArchitecture='*' publicKeyToken='6595b64144ccf1df' language='*'\"")

LRESULT CALLBACK WndProc(HWND hWnd, UINT message, WPARAM wParam, LPARAM lParam)
{
	switch (message)
	{
		case WM_PAINT:
		{
			PAINTSTRUCT ps;
			HDC hdc = BeginPaint(hWnd, &ps);

			LPCTSTR str[] = {
				_T("Количество сравнений"),
				_T("Метод дления"),
				_T("Метод середины кадратов"),
				_T("Метод свёртывания"),
				_T("Метод умножения"),
				_T("Метод открытой адресацией"),
				_T("Метод цепочек")
			};

			TextOut(hdc, 25, 20, str[0], lstrlen(str[0]));
			TextOut(hdc, 20, 80, str[1], lstrlen(str[1]));
			TextOut(hdc, 20, 120, str[2], lstrlen(str[2]));
			TextOut(hdc, 20, 160, str[3], lstrlen(str[3]));
			TextOut(hdc, 20, 200, str[4], lstrlen(str[4]));
			TextOut(hdc, 20, 310, str[5], lstrlen(str[5]));
			TextOut(hdc, 20, 350, str[6], lstrlen(str[6]));

			HPEN hPen = CreatePen(PS_SOLID, 5, RGB(0, 0, 0));
			SelectObject(hdc, hPen);

			POINT pt;
			MoveToEx(hdc, 0, 290, &pt);
			LineTo(hdc, 433, 290);

			DeleteObject(hPen);
			EndPaint(hWnd, &ps);

			break;
		}

		case WM_CREATE:
		{
			CreateWindow(_T("edit"), _T("0"), WS_CHILD | WS_VISIBLE | WS_BORDER | ES_NUMBER, 275, 20, 120, 30, hWnd, NULL, NULL, NULL);
			CreateWindow(_T("edit"), NULL, WS_CHILD | WS_VISIBLE | WS_BORDER | ES_READONLY, 275, 75, 120, 30, hWnd, NULL, NULL, NULL);
			CreateWindow(_T("edit"), NULL, WS_CHILD | WS_VISIBLE | WS_BORDER | ES_READONLY, 275, 115, 120, 30, hWnd, NULL, NULL, NULL);
			CreateWindow(_T("edit"), NULL, WS_CHILD | WS_VISIBLE | WS_BORDER | ES_READONLY, 275, 155, 120, 30, hWnd, NULL, NULL, NULL);
			CreateWindow(_T("edit"), NULL, WS_CHILD | WS_VISIBLE | WS_BORDER | ES_READONLY, 275, 195, 120, 30, hWnd, NULL, NULL, NULL);
			CreateWindow(_T("edit"), NULL, WS_CHILD | WS_VISIBLE | WS_BORDER | ES_READONLY, 275, 300, 120, 30, hWnd, NULL, NULL, NULL);
			CreateWindow(_T("edit"), NULL, WS_CHILD | WS_VISIBLE | WS_BORDER | ES_READONLY, 275, 340, 120, 30, hWnd, NULL, NULL, NULL);

			CreateWindow(_T("button"), _T("Вычислить"), WS_CHILD | WS_VISIBLE, 166, 240, 100, 30, hWnd, NULL, NULL, NULL);
			CreateWindow(_T("button"), _T("Сравнить"), WS_CHILD | WS_VISIBLE, 166, 390, 100, 30, hWnd, NULL, NULL, NULL);

			break;
		}

		case WM_DESTROY:
		{
			PostQuitMessage(0);
			break;
		}

		default:
			return DefWindowProc(hWnd, message, wParam, lParam);
	}

	return EXIT_SUCCESS;
}


INT APIENTRY _tWinMain(
	_In_ HINSTANCE hInstance,
	_In_opt_ HINSTANCE hPrevInstance,
	_In_ LPWSTR lpCmdLine,
	_In_ INT nCmdShow)
{
	WNDCLASS wc = { 0 };
	wc.lpfnWndProc = WndProc;
	wc.lpszClassName = _T("MainWindow");

	ATOM aResultRegisterClass = RegisterClass(&wc);
	if (aResultRegisterClass == FALSE)
		return EXIT_FAILURE;

	HWND hWnd = CreateWindow(wc.lpszClassName, NULL, WS_OVERLAPPEDWINDOW, 0, 0, 433, 480, NULL, NULL, hInstance, NULL);
	if (hWnd == NULL)
		return EXIT_FAILURE;

	ShowWindow(hWnd, nCmdShow);

	BOOL bResultUpdateWindow = UpdateWindow(hWnd);
	if (bResultUpdateWindow == FALSE)
		return EXIT_FAILURE;

	MSG msg;
	while (GetMessage(&msg, NULL, 0, 0))
	{
		TranslateMessage(&msg);
		DispatchMessage(&msg);
	}

	return (INT)msg.wParam;
}
