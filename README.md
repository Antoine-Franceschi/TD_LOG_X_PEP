# TD_LOG_X_PEP

TDLOG

- De belles choses dans le `Makefile` pour te faciliter la vie, tu peux faire des choses comme `make build && make run`
- Ton site va pas apparaître sur localhost:5000. Il faut aller voir l'ip du host docker(accessible avec `make print_ip`)
- Préférable de bind sur http 80/https 443 port au lieu de 5000 pour un usage plus poussé
- Sensible aux attaques DoS, plutôt utiliser nginx que gunicorn pour un usage plus poussé
