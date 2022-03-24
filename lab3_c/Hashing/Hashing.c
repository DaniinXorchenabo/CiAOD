/******************************************************************************
	* File: HashMainFile.c
	* Description: The third laboratory work on the subject "DPSaA".
	* Created: 26 sep 2021
	* Author: Ilya Gromov
	* Email: t1m0shenko@yandex.ru

******************************************************************************/

#include <windows.h>
#include <tchar.h>

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

struct _node
{
	INT64 key;
	struct _node *nextNode;
};

typedef struct _node NODE;
typedef NODE FAR *LPNODE;
typedef LPNODE FAR *LPPNODE;


struct _arr_lppnode
{
	LPPNODE lppNodes;
	UINT64 length;
};

typedef struct _arr_lppnode ARRLPPNODE;
typedef ARRLPPNODE FAR *LPARRLPPNODE;


struct _array
{
	PINT64 data;
	UINT64 length;
};

typedef struct _array ARRAY;
typedef ARRAY FAR *LPARRAY;


_Success_(return != NULL)
INLINE STATIC _Ret_maybenull_ LPARRAY CALLBACK
CreateArray(
	_In_ REGISTER CONST UINT64 lengthArray)
{
	REGISTER LPARRAY lpArray = malloc(sizeof(ARRAY));
	if (lpArray == NULL)
		return NULL;

	lpArray->data = malloc(lengthArray * sizeof(INT64));
	if (lpArray->data == NULL)
		return NULL;

	lpArray->length = lengthArray;

	for (
		REGISTER UINT64 i = 0;
		i < lengthArray;
		++i)
		lpArray->data[i] = -1;

	return lpArray;
}

INLINE STATIC VOID CALLBACK
DeleteArray(
	_In_ REGISTER LPARRAY lpArray)
{
	free(lpArray->data);
	free(lpArray);
}

_Success_(return != NULL)
INLINE STATIC _Ret_maybenull_ LPARRLPPNODE CALLBACK
CreateChains(
	_In_ REGISTER CONST UINT64 lengthArrlppNode)
{
	REGISTER LPARRLPPNODE lpArrNode = malloc(sizeof(ARRLPPNODE));
	if (lpArrNode == NULL)
		return NULL;

	lpArrNode->lppNodes = calloc(lengthArrlppNode, sizeof(LPNODE));
	lpArrNode->length = lengthArrlppNode;

	return lpArrNode;
}

INLINE STATIC VOID CALLBACK
DeleteChains(
	_In_ REGISTER LPARRLPPNODE lpArrlppNode)
{
	for (
		REGISTER UINT64 i = 0;
		i < lpArrlppNode->length;
		++i)
	{
		while (lpArrlppNode->lppNodes[i] != NULL)
		{
			if (lpArrlppNode->lppNodes[i]->nextNode == NULL)
			{
				free(lpArrlppNode->lppNodes[i]);
				lpArrlppNode->lppNodes[i] = NULL;

				break;
			}

			REGISTER LPNODE iter = lpArrlppNode->lppNodes[i];
			while (iter->nextNode->nextNode != NULL)
				iter = iter->nextNode;

			free(iter->nextNode);
			iter->nextNode = NULL;
		}
	}

	free(lpArrlppNode->lppNodes);
	free(lpArrlppNode);
}


_Success_(return != EXIT_FAILURE)
INLINE STATIC BOOL CALLBACK
ChainsMethod(
	_Inout_ REGISTER LPARRLPPNODE lpArrlppNode,
	_In_ REGISTER CONST UINT64 hashCode,
	_In_ REGISTER CONST INT64 keyValue,
	_Out_opt_ REGISTER LPBOOL collision)
{
	if (lpArrlppNode->lppNodes[hashCode] == NULL)
	{
		lpArrlppNode->lppNodes[hashCode] = calloc(1, sizeof(NODE));
		if (lpArrlppNode->lppNodes[hashCode] == NULL)
			return EXIT_FAILURE;

		lpArrlppNode->lppNodes[hashCode]->key = keyValue;

		if (collision != NULL)
			*collision = FALSE;

		return EXIT_SUCCESS;
	}

	REGISTER LPNODE lpNode = lpArrlppNode->lppNodes[hashCode];
	for (;
		lpNode->nextNode != NULL;
		lpNode = lpNode->nextNode);

	lpNode->nextNode = calloc(1, sizeof(NODE));
	if (lpNode->nextNode == NULL)
		return EXIT_FAILURE;

	lpNode->nextNode->key = keyValue;

	if (collision != NULL)
		*collision = TRUE;

	return EXIT_SUCCESS;
}

_Success_(return != EXIT_SUCCESS)
INLINE STATIC BOOL CALLBACK
OpenAddressingMethod(
	_Inout_ REGISTER LPARRAY lpArray,
	_In_ REGISTER CONST UINT64 hashCode,
	_In_ REGISTER CONST INT64 keyValue,
	_Out_opt_ REGISTER LPBOOL collision)
{
	if (collision != NULL)
		*collision = FALSE;

	for (
		REGISTER UINT64 iter = hashCode;
		iter < lpArray->length;
		++iter)
	{
		if (lpArray->data[iter] == -1)
		{
			lpArray->data[iter] = keyValue;
			return EXIT_SUCCESS;
		}

		if (collision != NULL &&
			*collision == FALSE)
			*collision = TRUE;
	}

	for (
		REGISTER UINT64 iter = 0;
		iter < hashCode;
		++iter)
	{
		if (lpArray->data[iter] == -1)
		{
			lpArray->data[iter] = keyValue;
			return EXIT_SUCCESS;
		}

		if (collision != NULL &&
			*collision == FALSE)
			*collision = TRUE;
	}

	return EXIT_FAILURE;
}



INLINE STATIC UINT64 CALLBACK
hash_0(
	_In_ REGISTER CONST INT64 keyValue,
	_In_ REGISTER CONST UINT64 length)
{
	return keyValue % length;
}

INLINE STATIC UINT64 CALLBACK
hash_1(
	_In_ REGISTER CONST INT64 keyValue,
	_In_ REGISTER CONST UINT64 length)
{
	REGISTER CONST INT64 p = keyValue * keyValue;

	REGISTER UINT64 lp = 0;
	for (
		REGISTER UINT64 i = p;
		i > 0; i /= 10,
		++lp);

	REGISTER UINT64 lm = 0;
	for (
		REGISTER UINT64 i = length;
		i > 0;
		i /= 10, ++lm);
	--lm;

	if (lm > lp)
		return p;

	REGISTER CONST UINT64 ll = (CONST UINT64)((lp - lm) * .5);
	REGISTER CONST UINT64 lr = (CONST UINT64)((lp - lm) * .5 + .5);

	REGISTER UINT64 llv = 1;
	for (
		REGISTER UINT64 i = 0;
		i < lp - ll;
		++i, llv *= 10);

	REGISTER UINT64 lrv = 1;
	for (
		REGISTER UINT64 i = 0;
		i < lr;
		++i, lrv *= 10);

	return p % llv / lrv;
}

INLINE STATIC UINT64 CALLBACK
hash_2(
	_In_ REGISTER CONST INT64 keyValue,
	_In_ REGISTER CONST UINT64 length)
{
	REGISTER UINT64 sum = 0;
	for (
		REGISTER UINT64 iter = keyValue;
		iter % length;
		sum += iter % length, iter /= length);

	return sum % length;
}

INLINE STATIC UINT64 CALLBACK
hash_3(
	_In_ REGISTER CONST INT64 keyValue,
	_In_ REGISTER CONST UINT64 length)
{
	REGISTER CONST DOUBLE ka = keyValue * .6180339887498948;
	return (UINT64)(length * (ka - (INT64)ka));
}

STATIC UINT64(CALLBACK *
	hashFunctions[])(
		_In_ REGISTER CONST INT64,
		_In_ REGISTER CONST UINT64)
	= { hash_0, hash_1, hash_2, hash_3 };

#ifdef ENABLE_HASH_4
INLINE STATIC UINT64 CALLBACK
hash_4(
	_In_ REGISTER CONST INT64 k,
	_In_ REGISTER CONST UINT64 m)
{
	return hashFunctions[rand() % 4](k, m);
}
#endif

_Success_(return == TRUE)
INLINE STATIC BOOL CALLBACK
FindChains(
	_In_ REGISTER CONST LPARRLPPNODE lpArrlppNode,
	_In_ REGISTER CONST INT64 keyValue,
	_In_opt_ REGISTER CONST UINT64(CALLBACK *
		hashFunction)(
			_In_ REGISTER CONST INT64,
			_In_ REGISTER CONST UINT64),
	_Out_opt_ REGISTER PUINT64 comparisons)
{
	if (hashFunction == NULL)
		hashFunction = *hashFunctions;

	if (comparisons == NULL)
		return FALSE;

	++ *comparisons;

	for (
		REGISTER LPNODE iter
		= lpArrlppNode->lppNodes[hashFunction(keyValue, lpArrlppNode->length)];
		iter != NULL;
		iter = iter->nextNode)
	{
		++ *comparisons;

		if (iter->key == keyValue)
			return TRUE;
	}

	return FALSE;
}

_Success_(return == TRUE)
INLINE STATIC BOOL CALLBACK
FindArray(
	_In_ REGISTER CONST LPARRAY lpArray,
	_In_ REGISTER CONST INT64 keyValue,
	_In_opt_ REGISTER CONST UINT64(CALLBACK *
		hashFunction)(
			_In_ REGISTER CONST INT64,
			_In_ REGISTER CONST UINT64),
	_Out_opt_ REGISTER PUINT64 comparisons)
{
	if (comparisons == NULL)
		return FALSE;

	if (hashFunction == NULL)
		hashFunction = *hashFunctions;

	REGISTER CONST UINT64 h = hashFunction(keyValue, lpArray->length);
	REGISTER UINT64 iter = h;

	++ *comparisons;

	for (;	
		iter < lpArray->length && lpArray->data[iter] != -1;
		++iter)
	{
		++ *comparisons;

		if (lpArray->data[iter] == keyValue)
			return TRUE;
	}

	for (
		iter = 0;
		iter < h && lpArray->data[iter] != -1;
		++iter)
	{
		++ *comparisons;

		if (lpArray->data[iter] == keyValue)
			return TRUE;
	}

	return FALSE;
}

STATIC BOOL(CALLBACK *
	FindFuncions[])(
		_In_ REGISTER CONST LPVOID,
		_In_ REGISTER CONST INT64,
		_In_opt_ REGISTER CONST UINT64(CALLBACK *)(
			_In_ REGISTER CONST INT64,
			_In_ REGISTER CONST UINT64),
		_Out_opt_ REGISTER PUINT64)
	= { FindArray, FindChains };


_Success_(return != EXIT_FAILURE)
INLINE STATIC LRESULT CALLBACK
WndProc(
	_In_ CONST HWND hWnd,
	_In_ CONST UINT message,
	_In_ CONST WPARAM wParam,
	_In_ CONST LPARAM lParam)
{
	STATIC HWND outputFields[7];
	STATIC UINT64 betterHashFunction;

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
			outputFields[0] = CreateWindow(_T("edit"), _T("1"), WS_CHILD | WS_VISIBLE | WS_BORDER | ES_NUMBER, 275, 20, 120, 30, hWnd, (HMENU)EDIT_0, NULL, NULL);

			outputFields[1] = CreateWindow(_T("edit"), NULL, WS_CHILD | WS_VISIBLE | WS_BORDER | ES_READONLY, 275, 75, 120, 30, hWnd, (HMENU)EDIT_1, NULL, NULL);
			outputFields[2] = CreateWindow(_T("edit"), NULL, WS_CHILD | WS_VISIBLE | WS_BORDER | ES_READONLY, 275, 115, 120, 30, hWnd, (HMENU)EDIT_2, NULL, NULL);
			outputFields[3] = CreateWindow(_T("edit"), NULL, WS_CHILD | WS_VISIBLE | WS_BORDER | ES_READONLY, 275, 155, 120, 30, hWnd, (HMENU)EDIT_3, NULL, NULL);
			outputFields[4] = CreateWindow(_T("edit"), NULL, WS_CHILD | WS_VISIBLE | WS_BORDER | ES_READONLY, 275, 195, 120, 30, hWnd, (HMENU)EDIT_4, NULL, NULL);
			outputFields[5] = CreateWindow(_T("edit"), NULL, WS_CHILD | WS_VISIBLE | WS_BORDER | ES_READONLY, 275, 300, 120, 30, hWnd, (HMENU)EDIT_5, NULL, NULL);
			outputFields[6] = CreateWindow(_T("edit"), NULL, WS_CHILD | WS_VISIBLE | WS_BORDER | ES_READONLY, 275, 340, 120, 30, hWnd, (HMENU)EDIT_6, NULL, NULL);

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
					CONST INT iResultGetWindowText
						= GetWindowText(*outputFields, numberOfComparisonsStr, IOBUFFER);
					if (iResultGetWindowText == FALSE)
						return EXIT_FAILURE;

					UINT64 numberOfComparisons;
					CONST INT iResult_stscanf_s
						= _stscanf_s(numberOfComparisonsStr, _T("%I64u"), &numberOfComparisons);
					if (iResult_stscanf_s <= FALSE)
						return EXIT_FAILURE;

					if (numberOfComparisons <= 0)
						return EXIT_SUCCESS;

					UINT64 wins[4] CLEARARR;
					for (
						UINT64 count = 0;
						count < numberOfComparisons;
						++count)
					{
						CONST UINT64 arrNodeSize = 1000;
						LPARRLPPNODE lpArrlppNode[4];

						for (
							UINT64 iter = 0;
							iter < 4;
							++iter)
						{
							lpArrlppNode[iter] = CreateChains(arrNodeSize);
							if (lpArrlppNode[iter] == NULL)
								return EXIT_FAILURE;
						}

						UINT64 colls[4] CLEARARR;
						for (
							UINT64 iter = 0;
							iter < arrNodeSize;
							++iter)
						{
							CONST INT64 rnd = rand() % 65000;
							for (
								UINT64 iter2 = 0;
								iter2 < 4;
								++iter2)
							{
								BOOL coll;
								CONST BOOL bResultChains = ChainsMethod(
									lpArrlppNode[iter2],
									hashFunctions[iter2](rnd, arrNodeSize),
									rnd,
									&coll);
								if (bResultChains != FALSE)
								{
									return EXIT_FAILURE;
								}
								colls[iter2] += coll;
							}
						}

						UINT64 min = *colls;
						UINT64 index = 0;

						for (
							UINT64 iter = 0;
							iter < 4;
							++iter)
						{
							if (min > colls[iter])
							{
								min = colls[iter];
								index = iter;
							}
							DeleteChains(lpArrlppNode[iter]);
						}
						++wins[index];
					}

					UINT64 max = *wins;

					for (
						UINT64 i = 0;
						i < 4;
						++i)
					{
						TCHAR outputBuffer[IOBUFFER] CLEARARR;
						CONST INT iResult_stprintf_s
							= _stprintf_s(outputBuffer, IOBUFFER, _T("%I64u"), wins[i]);
						if (iResult_stprintf_s <= FALSE)
							return EXIT_FAILURE;

						CONST BOOL bResultSetWindowText
							= SetWindowText(outputFields[i + 1], outputBuffer);
						if (bResultSetWindowText == FALSE)
							return EXIT_FAILURE;

						if (max < wins[i])
						{
							max = wins[i];
							betterHashFunction = i;
						}
					}
					break;
				}

				case BUTT_1:
				{
					CONST UINT64 hashTableLength = 10000;
					LPARRAY lpArray = CreateArray(hashTableLength);
					LPARRLPPNODE lpArrlppNode = CreateChains(hashTableLength);

					if (!lpArray)
						return EXIT_FAILURE;

					if (!lpArrlppNode)
					{
						DeleteArray(lpArray);
						return EXIT_FAILURE;
					}

					for (
						UINT64 iter = 0;
						iter < hashTableLength;
						++iter)
					{
						CONST INT64 keyValue = rand() % 10000;
						CONST UINT64 hashCode
							= hashFunctions[betterHashFunction](keyValue, hashTableLength);

						OpenAddressingMethod(lpArray, hashCode, keyValue, NULL);
						ChainsMethod(lpArrlppNode, hashCode, keyValue, NULL);
					}

					PINT64 arrayKeys = malloc(10000 * sizeof(INT64));
					if (!arrayKeys)
					{
						DeleteArray(lpArray);
						DeleteChains(lpArrlppNode);

						return EXIT_FAILURE;
					}

					for (
						UINT64 iter = 0;
						iter < hashTableLength;
						++iter)
						arrayKeys[iter] = rand() % 20000;

					UINT64 allComps[2] CLEARARR;
					UINT64 found[2] CLEARARR;
					ULONGLONG times[2];
					CONST LPVOID containers[] = { lpArray, lpArrlppNode };

					for (
						UINT64 iter = 0;
						iter < 2;
						++iter)
					{
						times[iter] = GetTickCount64();
						for (UINT64
							iter2 = 0;
							iter2 < hashTableLength;
							++iter2)
							found[iter] += FindFuncions[iter](
								containers[iter],
								arrayKeys[iter2],
								hashFunctions[betterHashFunction],
								allComps + iter);
						times[iter] = GetTickCount64() - times[iter];
					}

					free(arrayKeys);

					DOUBLE allCompsS[2];
					for (UINT64 iter = 0; iter < 2; ++iter)
						allCompsS[iter] = (DOUBLE)allComps[iter] / hashTableLength;

					DeleteChains(lpArrlppNode);
					DeleteArray(lpArray);

					for (
						UINT64 iter = 0;
						iter < 2;
						++iter)
					{
						TCHAR outputBuffer[IOBUFFER] CLEARARR;
						CONST INT iResult_stprintf_s
							= _stprintf_s(
								outputBuffer, IOBUFFER,
								_T("%I64u %.2f %I64u"),
								times[iter], allCompsS[iter], found[iter]);
						if (iResult_stprintf_s <= FALSE)
							return EXIT_FAILURE;

						CONST BOOL bResultSetWindowText
							= SetWindowText(outputFields[iter + 5], outputBuffer);
						if (bResultSetWindowText == FALSE)
							return EXIT_FAILURE;
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
			return DefWindowProc(hWnd, message, wParam, lParam);
	}

	return EXIT_SUCCESS;
}


INT APIENTRY
_tWinMain(
	_In_ HINSTANCE hInstance,
	_In_opt_ HINSTANCE hPrevInstance,
	_In_ LPWSTR lpCmdLine,
	_In_ INT nCmdShow)
{
	(VOID)lpCmdLine;
	(VOID)hPrevInstance;

	WNDCLASS wc CLEARARR;
	wc.lpfnWndProc = WndProc;
	wc.hbrBackground = (HBRUSH)(COLOR_WINDOW + 1);
	wc.lpszClassName = _T("MainWindow");

	CONST ATOM aResultRegisterClass = RegisterClass(&wc);
	if (aResultRegisterClass == FALSE)
		return EXIT_FAILURE;

	CONST HWND hWnd = CreateWindow(
		wc.lpszClassName,
		NULL, WS_OVERLAPPEDWINDOW,
		0, 0, 433, 480,
		NULL, NULL, hInstance, NULL);
	if (hWnd == NULL)
		return EXIT_FAILURE;

	ShowWindow(hWnd, nCmdShow);

	CONST BOOL bResultUpdateWindow = UpdateWindow(hWnd);
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