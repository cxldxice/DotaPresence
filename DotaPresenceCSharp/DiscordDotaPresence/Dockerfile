FROM mcr.microsoft.com/dotnet/runtime:5.0 AS base
WORKDIR /app

FROM mcr.microsoft.com/dotnet/sdk:5.0 AS build
WORKDIR /src
COPY ["DiscordDotaPresence/DiscordDotaPresence.csproj", "DiscordDotaPresence/"]
RUN dotnet restore "DiscordDotaPresence/DiscordDotaPresence.csproj"
COPY . .
WORKDIR "/src/DiscordDotaPresence"
RUN dotnet build "DiscordDotaPresence.csproj" -c Release -o /app/build

FROM build AS publish
RUN dotnet publish "DiscordDotaPresence.csproj" -c Release -o /app/publish

FROM base AS final
WORKDIR /app
COPY --from=publish /app/publish .
ENTRYPOINT ["dotnet", "DiscordDotaPresence.dll"]
