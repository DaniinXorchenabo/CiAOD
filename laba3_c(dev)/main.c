#include <windows.h>
#include <tchar.h>
#include <stdio.h>

#pragma warning(disable: 4715) // for hash_4()
#pragma comment(linker,"\"/manifestdependency:type='win32' \
name='Microsoft.Windows.Common-Controls' version='6.0.0.0' \
processorArchitecture='*' publicKeyToken='6595b64144ccf1df' language='*'\"")


typedef struct _node
{
	UINT64 hash;
	struct _node *next;
} NODE;

typedef NODE FAR *LPNODE;
typedef LPNODE FAR *LPPNODE;


typedef struct _arrnode
{
	LPPNODE lpNodes;
	UINT64 len;
} ARRNODE;

typedef ARRNODE FAR *LPARRNODE;


typedef struct _array
{
	PINT64 arr;
	UINT64 len;
} ARRAY;

typedef ARRAY FAR *LPARRAY;


LPARRAY CALLBACK CreateArray(_In_ CONST UINT64 len)
{
	LPARRAY lpArray = malloc(sizeof(ARRAY));
	if (lpArray == NULL)
	{
		return NULL;
	}

	lpArray->arr = malloc(len * sizeof(INT64));
	if (lpArray->arr == NULL)
	{
		return NULL;
	}

	lpArray->len = len;
	memset(lpArray->arr, -1, len);
	return lpArray;
}

VOID CALLBACK DeleteArray(_In_ LPARRAY lpArray)
{
	free(lpArray->arr);
	free(lpArray);
}


LPARRNODE CALLBACK CreateChains(_In_ CONST UINT64 len)
{
	LPARRNODE lpArrNode = malloc(sizeof(ARRNODE));
	if (lpArrNode == NULL)
	{
		return NULL;
	}

	lpArrNode->lpNodes = calloc(len, sizeof(LPNODE));
	lpArrNode->len = len;

	return lpArrNode;
}

VOID CALLBACK DeleteChains(_In_ LPARRNODE lpArrnode)
{
	for (UINT64 i = 0; i < lpArrnode->len; ++i)
	{
		while (lpArrnode->lpNodes[i] != NULL)
		{
			if (lpArrnode->lpNodes[i]->next == NULL)
			{
				free(lpArrnode->lpNodes[i]);
				lpArrnode->lpNodes[i] = NULL;

				break;
			}

			LPNODE iter = lpArrnode->lpNodes[i];
			while (iter->next->next != NULL)
			{
				iter = iter->next;
			}

			free(iter->next);
			iter->next = NULL;
		}
	}
	free(lpArrnode->lpNodes);
	free(lpArrnode);
}


BOOL CALLBACK Chains(_Inout_ LPARRNODE lpArrnode, _In_ CONST UINT64 h, _Out_opt_ LPBOOL coll)
{
	if (lpArrnode->lpNodes[h] == NULL)
	{
		lpArrnode->lpNodes[h] = calloc(1, sizeof(NODE));
		if (lpArrnode->lpNodes[h] == NULL)
		{
			return EXIT_FAILURE;
		}

		lpArrnode->lpNodes[h]->hash = h;
		*coll = FALSE;
		return EXIT_SUCCESS;
	}

	LPNODE lpNode = lpArrnode->lpNodes[h];
	while (lpNode->next != NULL)
	{
		lpNode = lpNode->next;
	}

	lpNode->next = calloc(1, sizeof(NODE));
	if (lpNode->next == NULL)
	{
		return EXIT_FAILURE;
	}

	lpNode->next->hash = h;
	*coll = TRUE;
	return EXIT_SUCCESS;
}

BOOL CALLBACK OpenAddressing(_Inout_ LPARRAY arr, _In_ CONST UINT64 h, _Out_opt_ LPBOOL coll)
{
	*coll = FALSE;

	for (UINT64 i = h; i < arr->len; ++i)
	{
		if (arr->arr[i] == -1)
		{
			arr->arr[i] = h;
			return EXIT_SUCCESS;
		}

		if (*coll == FALSE)
		{
			*coll = TRUE;
		}
	}

	return EXIT_FAILURE;
}


UINT64 CALLBACK hash_0(_In_ CONST INT64 k, _In_ CONST UINT64 m)
{
	return k % m;
}

UINT64 CALLBACK hash_1(_In_ CONST INT64 k, _In_ CONST UINT64 m)
{
	CONST INT64 p = k * k;
	UINT64 lp = 0;
	for (UINT64 i = p; i > 0; i /= 10, ++lp);

	UINT64 lm = 0;
	for (UINT64 i = m; i > 0; i /= 10, ++lm);
	--lm;

	if (lm > lp)
	{
		return p;
	}

	CONST UINT64 ll = (CONST UINT64)((lp - lm) * .5);
	CONST UINT64 lr = (CONST UINT64)((lp - lm) * .5 + .5);

	UINT64 llv = 1;
	for (UINT64 i = 0; i < lp - ll; ++i, llv *= 10);

	UINT64 lrv = 1;
	for (UINT64 i = 0; i < lr; ++i, lrv *= 10);

	return p % llv / lrv;
}

UINT64 CALLBACK hash_2(_In_ CONST INT64 k, _In_ CONST UINT64 m)
{
	UINT64 s = 0;
	for (UINT64 i = k; i % m; s += i % m, i /= m);

	return s % m;
}

UINT64 CALLBACK hash_3(_In_ CONST INT64 k, _In_ CONST UINT64 m)
{
	CONST FLOAT ka = k * 0.618f;
	return (UINT64)(m * (ka - (INT64)ka));
}

UINT64 CALLBACK hash_4(_In_ CONST INT64 k, _In_ CONST UINT64 m)
{
	switch (rand() % 4)
	{
		case 0: return hash_0(k, m); break;
		case 1: return hash_1(k, m); break;
		case 2: return hash_2(k, m); break;
		case 3: return hash_3(k, m); break;
	}
}


#define EDIT_0 1000
#define EDIT_1 1001
#define EDIT_2 1002
#define EDIT_3 1003
#define EDIT_4 1004
#define EDIT_5 1005
#define EDIT_6 1006

#define BUTT_0 2000
#define BUTT_1 2001

HWND edits[7];


LRESULT CALLBACK WndProc(HWND hWnd, UINT message, WPARAM wParam, LPARAM lParam)
{
	switch (message)
	{
		case WM_PAINT:
		{
			PAINTSTRUCT ps;
			CONST HDC hdc = BeginPaint(hWnd, &ps);

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

			CONST HPEN hPen = CreatePen(PS_SOLID, 5, RGB(0, 0, 0));
			SelectObject(hdc, hPen);

			MoveToEx(hdc, 0, 290, NULL);
			LineTo(hdc, 433, 290);

			EndPaint(hWnd, &ps);
			DeleteObject(hPen);
			DeleteObject(hdc);

			break;
		}

		case WM_CREATE:
		{
			edits[0] = CreateWindow(_T("edit"), _T("1"), WS_CHILD | WS_VISIBLE | WS_BORDER | ES_NUMBER, 275, 20, 120, 30, hWnd, (HMENU)EDIT_0, NULL, NULL);

			edits[1] = CreateWindow(_T("edit"), NULL, WS_CHILD | WS_VISIBLE | WS_BORDER | ES_READONLY, 275, 75, 120, 30, hWnd, (HMENU)EDIT_1, NULL, NULL);
			edits[2] = CreateWindow(_T("edit"), NULL, WS_CHILD | WS_VISIBLE | WS_BORDER | ES_READONLY, 275, 115, 120, 30, hWnd, (HMENU)EDIT_2, NULL, NULL);
			edits[3] = CreateWindow(_T("edit"), NULL, WS_CHILD | WS_VISIBLE | WS_BORDER | ES_READONLY, 275, 155, 120, 30, hWnd, (HMENU)EDIT_3, NULL, NULL);
			edits[4] = CreateWindow(_T("edit"), NULL, WS_CHILD | WS_VISIBLE | WS_BORDER | ES_READONLY, 275, 195, 120, 30, hWnd, (HMENU)EDIT_4, NULL, NULL);
			edits[5] = CreateWindow(_T("edit"), NULL, WS_CHILD | WS_VISIBLE | WS_BORDER | ES_READONLY, 275, 300, 120, 30, hWnd, (HMENU)EDIT_5, NULL, NULL);
			edits[6] = CreateWindow(_T("edit"), NULL, WS_CHILD | WS_VISIBLE | WS_BORDER | ES_READONLY, 275, 340, 120, 30, hWnd, (HMENU)EDIT_6, NULL, NULL);

			CreateWindow(_T("button"), _T("Вычислить"), WS_CHILD | WS_VISIBLE, 166, 240, 100, 30, hWnd, (HMENU)BUTT_0, NULL, NULL);
			CreateWindow(_T("button"), _T("Сравнить"), WS_CHILD | WS_VISIBLE, 166, 390, 100, 30, hWnd, (HMENU)BUTT_1, NULL, NULL);

			break;
		}

		case WM_COMMAND:
		{
			switch (LOWORD(wParam))
			{
				case BUTT_0:
				{
					TCHAR numberOfComparisonsStr[16] = { 0 };

					CONST INT iResultGetWindowText = GetWindowText(edits[0], numberOfComparisonsStr, 16);
					if (iResultGetWindowText == FALSE)
					{
						return EXIT_FAILURE;
					}

					UINT64 numberOfComparisons;
					CONST INT iResult_stscanf_s = _stscanf_s(numberOfComparisonsStr, _T("%I64u"), &numberOfComparisons);
					if (iResult_stscanf_s <= FALSE)
					{
						return EXIT_FAILURE;
					}

					UINT64 colls[4] = { 0 };
					for (UINT64 c = 0; c < numberOfComparisons; ++c)
					{
						CONST UINT64 arrsize = 1000;

						LPARRNODE lplpArrnode[4];
						for (UINT64 i = 0; i < 4; ++i)
						{
							lplpArrnode[i] = CreateChains(arrsize);
							if (lplpArrnode[i] == NULL)
							{
								return EXIT_FAILURE;
							}
						}

						BOOL coll;
						for (UINT64 i = 0; i < arrsize; ++i)
						{
							CONST USHORT rnd = rand() % 65000;

							BOOL bResultChains_1 = Chains(lplpArrnode[0], hash_0(rnd, arrsize), &coll);
							if (bResultChains_1 != FALSE)
							{
								return EXIT_FAILURE;
							}
							colls[0] += coll;

							BOOL bResultChains_2 = Chains(lplpArrnode[1], hash_1(rnd, arrsize), &coll);
							if (bResultChains_2 != FALSE)
							{
								return EXIT_FAILURE;
							}
							colls[1] += coll;

							BOOL bResultChains_3 = Chains(lplpArrnode[2], hash_2(rnd, arrsize), &coll);
							if (bResultChains_3 != FALSE)
							{
								return EXIT_FAILURE;
							}
							colls[2] += coll;

							BOOL bResultChains_4 = Chains(lplpArrnode[3], hash_3(rnd, arrsize), &coll);
							if (bResultChains_4 != FALSE)
							{
								return EXIT_FAILURE;
							}
							colls[3] += coll;
						}

						for (UINT64 i = 0; i < 4; ++i)
						{
							DeleteChains(lplpArrnode[i]);
						}
					}
					
					TCHAR outputBuffer[16] = { 0 };
					for (UINT64 i = 0; i < 4; ++i)
					{
						CONST INT iResult_stprintf_s = _stprintf_s(outputBuffer, 16, _T("%I64u"), colls[i]);
						if (iResult_stprintf_s <= FALSE)
						{
							return EXIT_FAILURE;
						}

						CONST BOOL bResultSetWindowText = SetWindowText(edits[i + 1], outputBuffer);
						if (bResultSetWindowText == FALSE)
						{
							return EXIT_FAILURE;
						}
					}
					break;
				}

				case BUTT_1:
				{
					//TODO: finish up

					break;
				}
			}
			break;
		}

		case WM_DESTROY:
		{
			PostQuitMessage(0);
			break;
		}

		default:
		{
			return DefWindowProc(hWnd, message, wParam, lParam);
		}
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
	wc.hbrBackground = (HBRUSH)COLOR_WINDOW;
	wc.lpszClassName = _T("MainWindow");

	CONST ATOM aResultRegisterClass = RegisterClass(&wc);
	if (aResultRegisterClass == FALSE)
	{
		return EXIT_FAILURE;
	}

	HWND hWnd = CreateWindow(wc.lpszClassName, NULL, WS_OVERLAPPEDWINDOW, 0, 0, 433, 480, NULL, NULL, hInstance, NULL);
	if (hWnd == NULL)
	{
		return EXIT_FAILURE;
	}

	ShowWindow(hWnd, nCmdShow);

	CONST BOOL bResultUpdateWindow = UpdateWindow(hWnd);
	if (bResultUpdateWindow == FALSE)
	{
		return EXIT_FAILURE;
	}

	MSG msg;
	while (GetMessage(&msg, NULL, 0, 0))
	{
		TranslateMessage(&msg);
		DispatchMessage(&msg);
	}

	return (INT)msg.wParam;
}