#include "CollisionHandling.h"

BOOL CALLBACK open_addressing(_In_ CONST UINT64 h, _Inout_ PUINT64 arr, _In_ CONST UINT64 m)
{
	for (UINT64 i = h; i < m; ++i)
	{
		if (arr[i] == -1)
		{
			arr[i] = h;
			return EXIT_SUCCESS;
		}
	}

	return EXIT_FAILURE;
}

BOOL CALLBACK chains(_In_ CONST INT h, _Inout_ LPNODE node, _In_ CONST INT m)
{
	if (node[h].next == NULL)
	{
		node[h].next = calloc(1, sizeof(NODE));
		if (node[h].next == NULL) return EXIT_FAILURE;

		node[h].next->hash = h;
	}
	else
	{
		LPNODE lpNode = node[h].next;

		while (lpNode->next != NULL)
			lpNode = lpNode->next;

		lpNode->next = calloc(1, sizeof(NODE));
		if (lpNode->next == NULL) return EXIT_FAILURE;

		lpNode->next->hash = h;
	}

	return EXIT_SUCCESS;
}