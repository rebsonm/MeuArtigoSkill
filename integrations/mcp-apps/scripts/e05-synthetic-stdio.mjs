/** E05 ONLY: launch private tunnel stdio with enforced fixed synthetic fixture inputs. */
import {createServer} from "../server.mjs";
import {StdioServerTransport} from "@modelcontextprotocol/sdk/server/stdio.js";
process.env.MEU_ARTIGO_E05_SYNTHETIC_ONLY="YES";
await createServer().connect(new StdioServerTransport());
