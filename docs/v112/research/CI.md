# Validation par commit

Point de départ : `ad2fc6b6e211ccb686052273221cb35f26e30bf6`.
[Run 43922540522](https://github.com/kikieaubonne-dot/vdn-research-agent/actions/runs/43922540522) :
460 tests hors ligne +460 en configuration personnelle isolée, Ubuntu et Windows.

## Code de cette livraison : CI vérifiée

Head PR : **`e84bb9649ac4ab169443c2b000c7f2c31fbceb37`**, base
`d23aafa6a190ff69d951730dd39566ed3e33f7a0`.
[Run 43934593777](https://github.com/kikieaubonne-dot/vdn-research-agent/actions/runs/43934593777).

| Environnement | Python | Hors ligne | Copie configuration personnelle | Conclusion job |
|---|---|---|---|---|
| Ubuntu GitHub Actions | 3.11 | 490 tests, 18,596 s, OK | 490 tests, 18,457 s, OK | success |
| Windows GitHub Actions | 3.11 | 490 tests, 85,209 s, OK | 490 tests, 80,989 s, OK | success |
| Linux local | 3.12.14 | 490 tests, 96,888 s, OK | 490 tests, 95,440 s, OK | success |

Journaux des jobs 133535755300 /133535755769 consultés après leur terminaison.
Aucun skip annoncé dans leurs résumés. Source/settings inchangés après les copies
personnelles. Les sockets sont interdits dans les suites et leurs sous-processus.
[Résumés CI exacts](proofs/ci-code.json) · [Validation locale](proofs/local-validation.json).

GitHub teste la référence synthétique de PR `8900f47` (e84bb96 sur d23aafa).
La PR #8 reste ouverte : ce mécanisme de CI ne publie aucune fusion dans sa base.
Un commit documentaire ultérieur ajoute ces preuves sans changer les empreintes
produit de `proofs/tested-files.json`. Sa CI est vérifiée séparément et liée dans
la description de PR, après publication.

## Frontières

Vrai processus MCP stdio exercé. Interface Claude Desktop, PC Windows utilisateur,
Studio/B3/C1 et Blender5.2 NON TESTÉS. Ces catégories ne sont pas validées par la CI.
Aucun benchmark de modèle local réel, aucune mesure de quota Claude ou de FPS.
