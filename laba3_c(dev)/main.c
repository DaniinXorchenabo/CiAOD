#include <windows.h>
#include <tchar.h>
#include <time.h>

#pragma comment(linker,"\"/manifestdependency:type='win32' \
name='Microsoft.Windows.Common-Controls' version='6.0.0.0' \
processorArchitecture='*' publicKeyToken='6595b64144ccf1df' language='*'\"")

#define EDIT_0 1000
#define EDIT_1 1001
#define EDIT_2 1002
#define EDIT_3 1003
#define EDIT_4 1004
#define EDIT_5 1005
#define EDIT_6 1006

#define BUTT_0 2000
#define BUTT_1 2001

#define STATIC static
#define INLINE inline
#define REGISTER register

#define CLEARARR = { 0 }
#define IOBUFFER 32


typedef struct _node
{
	INT64 key;
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


INLINE STATIC LPARRAY CALLBACK CreateArray(_In_ REGISTER CONST UINT64 len)
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

	for (REGISTER UINT64 i = 0; i < lpArray->len; ++i)
	{
		lpArray->arr[i] = -1;
	}

	return lpArray;
}

INLINE STATIC VOID CALLBACK DeleteArray(_In_ REGISTER LPARRAY lpArray)
{
	free(lpArray->arr);
	free(lpArray);
}


INLINE STATIC LPARRNODE CALLBACK CreateChains(_In_ REGISTER CONST UINT64 len)
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

INLINE STATIC VOID CALLBACK DeleteChains(_In_ REGISTER LPARRNODE lpArrnode)
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


INLINE STATIC BOOL CALLBACK Chains(
	_Inout_ REGISTER LPARRNODE lpArrnode,
	_In_ REGISTER CONST UINT64 h,
	_In_ REGISTER CONST INT64 k,
	_Out_opt_ REGISTER LPBOOL coll)
{
	if (h >= lpArrnode->len)
	{
		return EXIT_FAILURE;
	}

	if (lpArrnode->lpNodes[h] == NULL)
	{
		lpArrnode->lpNodes[h] = calloc(1, sizeof(NODE));
		if (lpArrnode->lpNodes[h] == NULL)
		{
			return EXIT_FAILURE;
		}

		lpArrnode->lpNodes[h]->key = k;

		if (coll != NULL)
		{
			*coll = FALSE;
		}

		return EXIT_SUCCESS;
	}

	REGISTER LPNODE lpNode = lpArrnode->lpNodes[h];
	for (; lpNode->next != NULL; lpNode = lpNode->next);

	lpNode->next = calloc(1, sizeof(NODE));
	if (lpNode->next == NULL)
	{
		return EXIT_FAILURE;
	}

	lpNode->next->key = k;

	if (coll != NULL)
	{
		*coll = TRUE;
	}

	return EXIT_SUCCESS;
}

INLINE STATIC BOOL CALLBACK OpenAddressing(
	_Inout_ REGISTER LPARRAY lpArr,
	_In_ REGISTER CONST UINT64 h,
	_In_ REGISTER CONST INT64 k,
	_Out_opt_ REGISTER LPBOOL coll)
{
	if (coll != NULL)
	{
		*coll = FALSE;
	}

	for (REGISTER UINT64 i = h; i < lpArr->len; ++i)
	{
		if (lpArr->arr[i] == -1)
		{
			lpArr->arr[i] = k;
			return EXIT_SUCCESS;
		}

		if (coll != NULL &&
			*coll == FALSE)
		{
			*coll = TRUE;
		}
	}

	return EXIT_FAILURE;
}

INLINE STATIC UINT64 CALLBACK hash_0(_In_ REGISTER CONST INT64 k, _In_ REGISTER CONST UINT64 m)
{
	return k % m;
}

INLINE STATIC UINT64 CALLBACK hash_1(_In_ REGISTER CONST INT64 k, _In_ REGISTER CONST UINT64 m)
{
	REGISTER CONST INT64 p = k * k;

	REGISTER UINT64 lp = 0;
	for (REGISTER UINT64 i = p; i > 0; i /= 10, ++lp);

	REGISTER UINT64 lm = 0;
	for (REGISTER UINT64 i = m; i > 0; i /= 10, ++lm);
	--lm;

	if (lm > lp)
	{
		return p;
	}

	REGISTER CONST UINT64 ll = (CONST UINT64)((lp - lm) * .5);
	REGISTER CONST UINT64 lr = (CONST UINT64)((lp - lm) * .5 + .5);

	REGISTER UINT64 llv = 1;
	for (REGISTER UINT64 i = 0; i < lp - ll; ++i, llv *= 10);

	REGISTER UINT64 lrv = 1;
	for (REGISTER UINT64 i = 0; i < lr; ++i, lrv *= 10);

	return p % llv / lrv;
}

INLINE STATIC UINT64 CALLBACK hash_2(_In_ REGISTER CONST INT64 k, _In_ REGISTER CONST UINT64 m)
{
	REGISTER UINT64 s = 0;
	for (REGISTER UINT64 i = k; i % m; s += i % m, i /= m);

	return s % m;
}

INLINE STATIC UINT64 CALLBACK hash_3(_In_ REGISTER CONST INT64 k, _In_ REGISTER CONST UINT64 m)
{
	REGISTER CONST DOUBLE ka = k * .6180339887498948;
	return (UINT64)(m * (ka - (INT64)ka));
}

STATIC UINT64(CALLBACK *CONST hashes[])(_In_ REGISTER CONST INT64, _In_ REGISTER CONST UINT64) = { hash_0, hash_1, hash_2, hash_3 };

/* not used */
//INLINE STATIC UINT64 CALLBACK hash_4(_In_ REGISTER CONST INT64 k, _In_ REGISTER CONST UINT64 m)
//{
//	return hashes[rand() % 4](k, m);
//}


INLINE STATIC BOOL CALLBACK FindChains(
	_In_ REGISTER CONST LPARRNODE lpArrnode,
	_In_ REGISTER CONST INT64 k,
	_In_opt_ REGISTER CONST UINT64 (CALLBACK *hashFunc)(_In_ REGISTER CONST INT64, _In_ REGISTER CONST UINT64),
	_Out_opt_ REGISTER PUINT64 comp)
{
	if (hashFunc == NULL)
	{
		hashFunc = *hashes;
	}

	for (REGISTER LPNODE iter = lpArrnode->lpNodes[hashFunc(k, lpArrnode->len)];
		iter != NULL;
		iter = iter->next)
	{
		if (iter->key == k)
		{
			return TRUE;
		}

		if (comp != NULL)
		{
			++*comp;
		}
	}

	return FALSE;
}

INLINE STATIC BOOL CALLBACK FindArray(
	_In_ REGISTER CONST LPARRAY lpArr,
	_In_ REGISTER CONST INT64 k,
	_In_opt_ REGISTER CONST UINT64(CALLBACK *hashFunc)(_In_ REGISTER CONST INT64, _In_ REGISTER CONST UINT64),
	_Out_opt_ REGISTER PUINT64 comp)
{
	if (hashFunc == NULL)
	{
		hashFunc = *hashes;
	}

	for (REGISTER UINT64 i = hashFunc(k, lpArr->len);
		i < lpArr->len && lpArr->arr[i] != -1;
		++i)
	{
		if (lpArr->arr[i] == k)
		{
			return TRUE;
		}

		if (comp != NULL)
		{
			++*comp;
		}
	}

	return FALSE;
}

STATIC BOOL(CALLBACK *CONST FindFunc[])(
	_In_ REGISTER CONST LPVOID,
	_In_ REGISTER CONST INT64,
	_In_opt_ REGISTER CONST UINT64(CALLBACK *)(_In_ REGISTER CONST INT64, _In_ REGISTER CONST UINT64),
	_Out_opt_ REGISTER PUINT64) = { FindArray, FindChains };


LRESULT CALLBACK WndProc(_In_ CONST HWND hWnd, _In_ CONST UINT message, _In_ CONST WPARAM wParam, _In_ CONST LPARAM lParam)
{
	STATIC HWND edits[7];
	STATIC UINT64 better;

	switch (message)
	{
		case WM_PAINT:
		{
			PAINTSTRUCT ps;
			CONST HDC hdc = BeginPaint(hWnd, &ps);

			LPCTSTR str[] = {
				_T("Количество сравнений"),
				_T("Метод деления"),
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
					TCHAR numberOfComparisonsStr[IOBUFFER] CLEARARR;
					CONST INT iResultGetWindowText = GetWindowText(*edits, numberOfComparisonsStr, IOBUFFER);
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

					if (numberOfComparisons <= 0)
					{
						return EXIT_SUCCESS;
					}

					UINT64 wins[4] CLEARARR;
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

						UINT64 colls[4] CLEARARR;
						for (UINT64 i = 0; i < arrsize; ++i)
						{
							CONST INT64 rnd = rand() % 65000;
							for (UINT64 j = 0; j < 4; ++j)
							{
								BOOL coll;
								CONST BOOL bResultChains = Chains(lplpArrnode[j], hashes[j](rnd, arrsize), rnd, &coll);
								if (bResultChains != FALSE)
								{
									return EXIT_FAILURE;
								}
								colls[j] += coll;
							}
						}
						
						UINT64 min = *colls;
						UINT64 index = 0;

						for (UINT64 i = 0; i < 4; ++i)
						{
							if (min > colls[i])
							{
								min = colls[i];
								index = i;
							}
							DeleteChains(lplpArrnode[i]);
						}
						++wins[index];
					}

					UINT64 max = *wins;

					for (UINT64 i = 0; i < 4; ++i)
					{
						TCHAR outputBuffer[IOBUFFER] CLEARARR;
						CONST INT iResult_stprintf_s = _stprintf_s(outputBuffer, IOBUFFER, _T("%I64u"), wins[i]);
						if (iResult_stprintf_s <= FALSE)
						{
							return EXIT_FAILURE;
						}

						CONST BOOL bResultSetWindowText = SetWindowText(edits[i + 1], outputBuffer);
						if (bResultSetWindowText == FALSE)
						{
							return EXIT_FAILURE;
						}

						if (max < wins[i])
						{
							max = wins[i];
							better = i;
						}
					}
					break;
				}

				case BUTT_1:
				{
					CONST UINT64 len = 10000;
					LPARRAY lpArray = CreateArray(len);
					LPARRNODE lpArrnode = CreateChains(len);

					for (UINT64 i = 0; i < len; ++i)
					{
						CONST INT64 k = rand() % 10000;
						CONST UINT64 h = hashes[better](k, len);

						OpenAddressing(lpArray, h, k, NULL);
						Chains(lpArrnode, h, k, NULL);
					}

					INT64 arrkey[10000];
					for (UINT64 i = 0; i < len; ++i)
					{
						arrkey[i] = rand() % 20000;
					}

					UINT64 allComps[2] CLEARARR;
					UINT64 finds[2] CLEARARR;
					DWORD times[2];
					CONST LPVOID containers[] = { lpArray, lpArrnode };

					for (UINT64 i = 0; i < 2; ++i)
					{
						times[i] = GetTickCount();
						for (REGISTER UINT64 j = 0; j < len; ++j)
						{
							finds[i] += !FindFunc[i](containers[i], arrkey[j], hashes[better], allComps + i);
						}
						times[i] = GetTickCount() - times[i];
					}

					allComps[0] /= len;
					allComps[1] /= len;

					DeleteChains(lpArrnode);
					DeleteArray(lpArray);

					for (UINT64 i = 0; i < 2; ++i)
					{
						TCHAR outputBuffer[IOBUFFER] CLEARARR;
						CONST INT iResult_stprintf_s = _stprintf_s(outputBuffer, IOBUFFER, _T("%d - %I64u - %I64u"), times[i], allComps[i], finds[i]);
						if (iResult_stprintf_s <= FALSE)
						{
							return EXIT_FAILURE;
						}

						CONST BOOL bResultSetWindowText = SetWindowText(edits[i + 5], outputBuffer);
						if (bResultSetWindowText == FALSE)
						{
							return EXIT_FAILURE;
						}
					}
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
	wc.hbrBackground = (HBRUSH)(COLOR_WINDOW + 1);
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