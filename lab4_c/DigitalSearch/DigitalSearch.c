#include "DigitalSearch.h"

DIGITAL_TREE
DTCreate(
	VOID)
{
	return calloc(1, sizeof(PNODE));
}

#pragma warning(disable: 4706)
#pragma warning(disable: 5045)

BOOL
DTInsert(
	DIGITAL_TREE dt,
	PINT data,
	INT size,
	PBOOL unique)
{
	PNODE rootTmp = *dt;
	INT i = 0;
	*unique = FALSE;

	if (!*dt)
	{
		*dt = calloc(1, sizeof(NODE));
		if (!*dt)
			return EXIT_FAILURE;

		*unique = TRUE;
		(*(PNODE *)dt)->data = data[i++];
	}

	PNODE root = *dt;

	for (; i < size && rootTmp; ++i)
	{
		if (rootTmp->data == data[i])
		{
			root = rootTmp;
			rootTmp = rootTmp->down;
		}
		else
		{
			while (rootTmp)
			{
				root = rootTmp;
				if (rootTmp->data == data[i])
				{
					rootTmp = rootTmp->down;
					break;
				}
				else if (!(rootTmp = rootTmp->next))
				{
					root->next = calloc(1, sizeof(NODE));
					if (!root->next)
						return EXIT_FAILURE;

					*unique = TRUE;

					root = root->next;
					root->data = data[i];
				}
			}
		}
	}

	if (i >= size && root->down && (!root->down->next || root->down->next->data != INT_MAX))
	{
		root = root->down;
		rootTmp = root;

		while (rootTmp)
		{
			root = rootTmp;
			rootTmp = rootTmp->next;
		}

		root->next = calloc(1, sizeof(NODE));
		if (!root->next)
			return EXIT_FAILURE;

		root->next->data = INT_MAX;
		*unique = TRUE;
	}

	for (; i < size; ++i)
	{
		root->down = calloc(1, sizeof(NODE));
		if (!root->down)
			return EXIT_FAILURE;

		root = root->down;
		root->data = data[i];

		if (!*unique)
		{
			root->next = calloc(1, sizeof(NODE));
			if (!root->next)
				return EXIT_FAILURE;

			root->next->data = INT_MAX;
		}

		*unique = TRUE;
	}

	return EXIT_SUCCESS;
}

#pragma warning(disable: 5045)
#pragma warning(default: 4706)

BOOL
DTFind(
	DIGITAL_TREE dt,
	PINT data,
	INT size,
	PBOOL res)
{
	PNODE root = *dt;
	*res = FALSE;

	for (INT i = 0; i < size; ++i)
	{
		if (!root)
			return EXIT_SUCCESS;

		if (root->data == data[i])
			root = root->down;
		else
		{
			while (TRUE)
			{
				if (root->data == data[i])
				{
					root = root->down;
					break;
				}
				else
				{
					root = root->next;
					if (!root)
						return EXIT_SUCCESS;
				}
			}
		}
	}

	if (root)
	{
		if (root->next && root->next->data == INT_MAX)
			*res = TRUE;
	}
	else
		*res = TRUE;
	
	return EXIT_SUCCESS;
}