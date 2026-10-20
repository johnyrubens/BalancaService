# BalancaService

Serviço desenvolvido para a LIVE! para integrar uma balança à tela **Recebimento de peças** de uma aplicação React.

O Python foi escolhido pela simplicidade de implementação e pela possibilidade de distribuir a solução em um único executável.

## Funcionamento

- Conecta-se à balança pela porta serial.
- Lê os dados de pesagem com o auxílio da DLL do fabricante.
- Envia os dados via webhooks para que a aplicação React receba e exiba o peso na tela **Recebimento de peças**.
