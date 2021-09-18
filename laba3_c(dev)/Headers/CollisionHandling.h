#pragma once
#include <windows.h>
#include "ChainsNode.h"

BOOL CALLBACK open_addressing(_In_ CONST UINT64, _Inout_ PUINT64, _In_ CONST UINT64);
BOOL CALLBACK chains(_In_ CONST INT, _Inout_ LPNODE, _In_ CONST INT);