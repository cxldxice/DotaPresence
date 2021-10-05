FROM mcr.microsoft.com/dotnet/runtime:5.0 AS base
WORKDIR /app

FROM mcr.microsoft.com/dotnet/sdk:5.0 AS build
WORKDIR /src
COPY ["DotaPresenceCSharp/DotaPresenceCSharp.csproj", "DotaPresenceCSharp/"]
RUN dotnet restore "DotaPresenceCSharp/DotaPresenceCSharp.csproj"
COPY . .
WORKDIR "/src/DotaPresenceCSharp"
RUN dotnet build "DotaPresenceCSharp.csproj" -c Release -o /app/build

FROM build AS publish
RUN dotnet publish "DotaPresenceCSharp.csproj" -c Release -o /app/publish

FROM base AS final
WORKDIR /app
COPY --from=publish /app/publish .
ENTRYPOINT ["dotnet", "DotaPresenceCSharp.dll"]
