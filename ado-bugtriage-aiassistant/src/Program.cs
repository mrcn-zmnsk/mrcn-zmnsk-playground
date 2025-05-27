using Microsoft.VisualStudio.Services.Common;
using TriageApp.Server.Service;

var builder = WebApplication.CreateBuilder(args);

// Add services to the container.

builder.Services.AddControllers();
// Learn more about configuring Swagger/OpenAPI at https://aka.ms/aspnetcore/swashbuckle
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();
builder.Services.AddMemoryCache();

builder.Services.AddSingleton<IAdoFacade>(
    new AdoFacade(
        orgUrl: builder.Configuration["ado:orgUrl"],
        project: builder.Configuration["ado:project"],
        pat: builder.Configuration["ado:pat"]
    )
);
builder.Services.AddSingleton<IAdoTriageAssistant, AdoTriageAssistant>();

var app = builder.Build();

app.UseDefaultFiles();
app.UseStaticFiles();

// Configure the HTTP request pipeline.
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseHttpsRedirection();

app.UseAuthorization();

app.MapControllers();

app.MapFallbackToFile("/index.html");

app.Run();
