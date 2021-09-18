#pragma once

typedef struct _node
{
	UINT64 hash;
	struct _node *next;
} NODE, FAR *LPNODE;