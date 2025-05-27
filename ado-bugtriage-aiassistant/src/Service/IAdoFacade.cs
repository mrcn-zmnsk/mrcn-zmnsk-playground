namespace TriageApp.Server.Service
{
    using System;
    using System.Threading.Tasks;

    public interface IAdoFacade
    {
        Task<string> GetADOItem(int itemId);
        Task<string> GetReproFromDocx(int itemId);
        Task<string> RunQuery(Guid queryId);
    }
}