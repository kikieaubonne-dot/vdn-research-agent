# Validation par commit

Point de départ vérifié : `ad2fc6b6e211ccb686052273221cb35f26e30bf6`.
[Run 43922540522](https://github.com/kikieaubonne-dot/vdn-research-agent/actions/runs/43922540522) :
Ubuntu et Windows réussis, 460 tests hors ligne +460 en configuration personnelle
isolée par OS. Cette preuve ne valide pas encore les nouvelles modifications.

La présente livraison conserve le workflow Python3.11 Ubuntu/Windows existant.
La CI du commit publié est vérifiée après publication ; les résultats par SHA sont
consignés dans la PR #8, puis dans ce document une fois constatés. Ne pas interpréter
un résultat local comme un succès Windows anticipé.

Local : Linux/Python3.12.14 ; journaux finaux et empreintes dans `proofs/`.
Tests hors ligne et configuration personnelle isolée séparés. Un processus MCP stdio
est réellement lancé, sans interface Desktop. Aucun test sur le PC Windows de
l’utilisateur ni dans Studio/Blender5.2 n’est déclaré.
