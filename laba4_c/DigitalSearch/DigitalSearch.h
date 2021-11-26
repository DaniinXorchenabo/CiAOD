#pragma once

#pragma warning(disable: 4668)
#include <windows.h>
#pragma warning(default: 4668)
#include <tchar.h>

#pragma warning(disable: 4820)
typedef struct _NODE
{
	INT data;
	struct _NODE *next;
	struct _NODE *down;

} NODE, *PNODE;
#pragma warning(default: 4820)

typedef PVOID *DIGITAL_TREE;

DIGITAL_TREE
DTCreate(
	VOID);

BOOL
DTInsert(
	DIGITAL_TREE dt,
	PINT data,
	INT size,
	PBOOL unique);

BOOL
DTFind(
	DIGITAL_TREE dt,
	PINT data,
	INT size,
	PBOOL res);