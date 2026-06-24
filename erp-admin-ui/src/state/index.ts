import { observable } from '@legendapp/state'

export const appState = observable({
  legacy: {
    connected: false as boolean,
    systemInfo: null as Record<string, unknown> | null,
    activeProfile: 'sap_ecc' as string,
  },
  modern: {
    connected: false as boolean,
    systemInfo: null as Record<string, unknown> | null,
    activeProfile: 's4hana' as string,
  },
})
