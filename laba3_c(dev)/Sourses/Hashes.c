#include "Hashes.h"

UINT64 CALLBACK hash_0(_In_ CONST INT64 k, _In_ CONST UINT64 m)
{
	return k % m;
}

UINT64 CALLBACK hash_1(_In_ CONST INT64 k, _In_ CONST UINT64 m)
{
	return 0;
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

UINT64 CALLBACK hash_universal(_In_ CONST INT64 k, _In_ CONST UINT64 m)
{
	switch (rand() % 4)
	{
		case 0:
			return hash_0(k, m);
			break;

		case 1:
			return hash_1(k, m);
			break;

		case 2:
			return hash_2(k, m);
			break;

		default:
			return hash_3(k, m);
			break;
	}
}