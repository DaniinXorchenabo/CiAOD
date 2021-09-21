#include <windows.h>
#include <tchar.h>
#include <time.h>

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


LPARRAY CALLBACK create_array(_In_ CONST UINT64 len)
{
	LPARRAY lpArray = malloc(sizeof(ARRAY));
	if (lpArray == NULL)
		return NULL;

	lpArray->arr = malloc(len * sizeof(INT64));
	if (lpArray->arr == NULL)
		return NULL;

	lpArray->len = len;
	memset(lpArray->arr, -1, len);
	return lpArray;
}

VOID CALLBACK delete_array(_In_ LPARRAY lpArray)
{
	free(lpArray->arr);
	free(lpArray);
}


LPARRNODE CALLBACK create_chains(_In_ CONST UINT64 len)
{
	LPARRNODE lpArrNode = malloc(sizeof(ARRNODE));
	if (lpArrNode == NULL)
		return NULL;

	lpArrNode->lpNodes = calloc(len, sizeof(LPNODE));
	lpArrNode->len = len;

	return lpArrNode;
}

VOID CALLBACK delete_chains(_In_ LPARRNODE lpArrnode)
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
				iter = iter->next;

			free(iter->next);
			iter->next = NULL;
		}
	}
	free(lpArrnode->lpNodes);
	free(lpArrnode);
}


BOOL CALLBACK chains(_Inout_ LPARRNODE lpArrnode, _In_ CONST UINT64 h, _Out_opt_ LPBOOL coll)
{
	if (lpArrnode->lpNodes[h] == NULL)
	{
		lpArrnode->lpNodes[h] = calloc(1, sizeof(NODE));
		if (lpArrnode->lpNodes[h] == NULL)
			return EXIT_FAILURE;

		lpArrnode->lpNodes[h]->hash = h;
		*coll = FALSE;
		return EXIT_SUCCESS;
	}

	LPNODE lpNode = lpArrnode->lpNodes[h];
	while (lpNode->next != NULL)
		lpNode = lpNode->next;

	lpNode->next = calloc(1, sizeof(NODE));
	if (lpNode->next == NULL)
		return EXIT_FAILURE;

	lpNode->next->hash = h;
	*coll = TRUE;
	return EXIT_SUCCESS;
}

BOOL CALLBACK open_addressing(_Inout_ LPARRAY arr, _In_ CONST UINT64 h, _Out_opt_ LPBOOL coll)
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
			*coll = TRUE;
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

	CONST UINT64 ll = (lp - lm) * .5;
	CONST UINT64 lr = (lp - lm) * .5 + .5;

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
	return m * (ka - (INT64)ka);
}

UINT64 CALLBACK hash_4(_In_ CONST INT64 k, _In_ CONST UINT64 m)
{
	switch (rand() % 3)
	{
		case 0: return hash_0(k, m); break;
		case 1: return hash_1(k, m); break;
		case 2: return hash_2(k, m); break;
		case 3: return hash_3(k, m); break;
	}
}


INT APIENTRY _tmain(INT argc, LPCTSTR argv[])
{
	// code ...
	return EXIT_SUCCESS;
}