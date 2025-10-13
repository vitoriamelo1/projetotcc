# Google Maps Integration

Este documento descreve como configurar e usar a integração do Google Maps no sistema de solicitação de corridas.

## Funcionalidades

### 1. Autocomplete de Endereços
- **Origem**: Campo com sugestões automáticas baseadas no Google Places API
- **Destino**: Campo com sugestões automáticas baseadas no Google Places API
- **Localização atual**: Botão para preencher automaticamente o endereço de origem com a localização atual do usuário

### 2. Visualização no Mapa
- **Mapa interativo**: Visualização dos endereços de origem e destino
- **Marcadores**: Origem (verde) e destino (vermelho)
- **Rota**: Traçado da rota entre origem e destino
- **Expansível**: Mapa pode ser mostrado/ocultado conforme necessário

### 3. Geocodificação
- **Reversa**: Converte coordenadas GPS em endereços legíveis
- **Direta**: Valida e padroniza endereços digitados

## Configuração

### 1. Obter API Key do Google Maps

1. Acesse o [Google Cloud Console](https://console.cloud.google.com/)
2. Crie um projeto ou selecione um existente
3. Vá para "APIs & Services" > "Credentials"
4. Clique em "Create Credentials" > "API Key"
5. Configure as restrições de API (recomendado):
   - **Application restrictions**: HTTP referrers
   - **API restrictions**: Selecione as APIs necessárias

### 2. Habilitar APIs Necessárias

No Google Cloud Console, habilite as seguintes APIs:

- **Maps JavaScript API**: Para exibir mapas interativos
- **Places API**: Para autocomplete de endereços
- **Geocoding API**: Para conversão entre coordenadas e endereços

### 3. Configurar no Django

Adicione a chave da API no arquivo `.env`:

```bash
GOOGLE_MAPS_API_KEY=your-google-maps-api-key-here
```

### 4. Configurar Restrições de Segurança (Recomendado)

Para produção, configure restrições no Google Cloud Console:

#### HTTP Referrers:
```
https://yourdomain.com/*
https://www.yourdomain.com/*
```

#### API Restrictions:
- Maps JavaScript API
- Places API
- Geocoding API

## Uso

### No Template
O formulário de solicitação de corrida (`_solicita_corrida_form.html`) inclui automaticamente:

1. **Campos com autocomplete**:
   ```html
   <input id="ride_endereco_origem" name="endereco_origem" ... autocomplete="off" />
   ```

2. **Botão de localização atual**:
   ```html
   <button id="get-current-location-btn" title="Usar localização atual">
   ```

3. **Mapa expansível**:
   ```html
   <div id="map-container" class="hidden">
     <div id="map" class="w-full h-64 bg-gray-200 rounded-lg"></div>
   </div>
   ```

### JavaScript APIs Disponíveis

As seguintes funções estão disponíveis globalmente:

- `initGoogleMaps()`: Inicializa o Google Maps
- `getCurrentLocation()`: Obtém a localização atual do usuário
- `toggleMap()`: Mostra/oculta o mapa
- `updateRoute()`: Atualiza a rota entre origem e destino

## Fallbacks e Tratamento de Erros

### 1. API Key Não Configurada
Se a chave da API não estiver configurada, o sistema:
- Oculta elementos dependentes do Google Maps
- Mantém funcionalidade básica do formulário
- Exibe avisos no console do navegador

### 2. Erro de Geolocalização
Para erros de GPS/localização:
- Mostra mensagens de erro específicas
- Permissão negada pelo usuário
- Localização não disponível
- Timeout de localização

### 3. Falha no Carregamento da API
- Timeout de 3 segundos para carregamento
- Oculta elementos dependentes se a API falhar
- Mantém funcionalidade do formulário

## Estilos e Interface

### Classes CSS Customizadas
- `.border-red-500`: Bordas vermelhas para campos com erro
- `.hidden`: Ocultar elementos (usado para toggle do mapa)
- `.fa-spinner.fa-spin`: Indicador de loading

### Ícones Font Awesome
- `fa-location-arrow`: Localização atual
- `fa-map`: Visualização do mapa
- `fa-chevron-down/up`: Expandir/recolher mapa
- `fa-spinner`: Loading

## Limitações e Considerações

### 1. Quotas da API
- Google Maps tem limites de uso gratuito
- Monitore o uso no Google Cloud Console
- Configure alertas de billing se necessário

### 2. Performance
- Scripts carregados assincronamente
- Mapa inicializado apenas quando necessário
- Autocomplete limitado ao Brasil (`componentRestrictions: { country: 'br' }`)

### 3. Privacidade
- Geolocalização requer permissão do usuário
- Dados de localização não são armazenados
- Apenas endereços de texto são salvos no banco

## Troubleshooting

### Problema: Mapa não carrega
**Solução**: Verifique se a API key está configurada e se a Maps JavaScript API está habilitada.

### Problema: Autocomplete não funciona
**Solução**: Verifique se a Places API está habilitada e se não há restrições bloqueando o domínio.

### Problema: Geolocalização falha
**Solução**: Certifique-se de que o site está sendo servido via HTTPS (necessário para geolocalização) ou localhost.

### Problema: "RefererNotAllowedMapError"
**Solução**: Configure os HTTP referrers corretos no Google Cloud Console.

## Desenvolvimento

### Ambiente Local
Para desenvolvimento local, use:
```bash
GOOGLE_MAPS_API_KEY=your-dev-api-key
```

### Ambiente de Produção
Configure restrições apropriadas e monitore o uso da API.

## Backup Manual
Caso o Google Maps não esteja disponível, o formulário mantém:
- Campos de texto para endereços
- Validação básica de campos obrigatórios
- Funcionalidade completa de solicitação de corridas